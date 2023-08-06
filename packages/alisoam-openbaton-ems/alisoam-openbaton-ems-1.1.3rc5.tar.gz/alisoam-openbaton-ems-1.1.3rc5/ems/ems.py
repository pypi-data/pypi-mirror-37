# Copyright (c) 2015 Fraunhofer FOKUS. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


# !/usr/bin/env python
import threading
import Queue
import os
import time
import logging
import ConfigParser
import pika
from receiver import on_message
from utils import get_map

__author__ = 'ogo'

log = logging.getLogger(__name__)

q = Queue.Queue()


def on_request(props, body):
    response = on_message(body)
    q.put({"props":props, "body": str(response)})

def thread_function(ch, method, properties, body):
    print 'new request'
    threading.Thread(target=on_request, args=(properties, body)).start()
    ch.basic_ack(delivery_tag=method.delivery_tag)


def publish_thread(broker_ip, broker_port, virtual_host, rabbit_credentials, heartbeat):
    sleep_time = 1
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=broker_ip, port=int(broker_port),
                                          virtual_host=virtual_host, credentials=rabbit_credentials, heartbeat_interval=int(heartbeat)))
            channel = connection.channel()
            while True:
                try:
                    o = q.get(block=True, timeout=10)
                    try:
                        props = o["props"]
                        body = o["body"]
                        channel.basic_publish(exchange='', routing_key=props.reply_to,
                                         properties=pika.BasicProperties(correlation_id=props.correlation_id, content_type='text/plain'),
                                         body=body)
                    except:
                        q.put(o)
                        raise
                except Queue.Empty:
                    connection.process_data_events(time_limit=10)
        except Exception:
            # logging.exception('')
            time.sleep(sleep_time)
            if (sleep_time < 10):
                sleep_time = sleep_time + 1
            else:
                sleep_time = sleep_time + 10


def main():
    sleep_time = 1
    logging_dir='/var/log/openbaton/'
    #logging_dir = 'log/openbaton/'
    if not os.path.exists(logging_dir):
        os.makedirs(logging_dir)
    logging.basicConfig(filename=logging_dir + '/ems-receiver.log', level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M')
    config_file_name = "/etc/openbaton/openbaton-ems.properties"
    log.debug(config_file_name)
    config = ConfigParser.ConfigParser()
    config.read(config_file_name)  # read config file
    _map = get_map(section='ems', config=config)  # get the data from map
    queue_type = _map.get("type")  # get type of the queue
    hostname = _map.get("hostname")
    username = _map.get("username")
    password = _map.get("password")
    autodel = _map.get("autodelete")
    heartbeat = _map.get("heartbeat")
    broker_port = _map.get("broker_port")
    exchange_name = _map.get("exchange")
    virtual_host = _map.get("virtual_host")
    queuedel = True
    if autodel == 'false':
        queuedel = False
    if not heartbeat:
        heartbeat = '60'
    if not exchange_name:
        exchange_name = 'openbaton-exchange'
    if not broker_port:
        broker_port = "5672"
    if not virtual_host:
        virtual_host = "/"
    if not queue_type:
        queue_type = "generic"
    log.info(
        "EMS configuration paramters are "
        "hostname: %s, username: %s, password: *****, autodel: %s, heartbeat: %s, exchange name: %s" % (
            hostname, username, autodel, heartbeat, exchange_name))
    broker_ip = _map.get("broker_ip")
    rabbit_credentials = pika.PlainCredentials(username, password)
    tt = threading.Thread(target=publish_thread, args=(broker_ip, broker_port, virtual_host, rabbit_credentials, heartbeat))
    tt.daemon = True
    tt.start()
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=broker_ip, port=int(broker_port),
                                          virtual_host=virtual_host, credentials=rabbit_credentials, heartbeat_interval=int(heartbeat)))
            channel = connection.channel()
            #channel.exchange_declare(exchange=exchange_name, type="topic", durable=True)
            #channel.queue_declare(queue='ems.%s.register'%queue_type, auto_delete=queuedel)
            channel.queue_bind(exchange=exchange_name, queue='ems.%s.register' % queue_type)
            channel.queue_declare(queue='vnfm.%s.actions' % hostname, auto_delete=queuedel)
            channel.queue_bind(exchange=exchange_name, queue='ems.%s.register' % queue_type)
            channel.queue_bind(exchange=exchange_name, queue='vnfm.%s.actions' % hostname)
            channel.basic_publish(exchange='', routing_key='ems.%s.register' % queue_type,
                                  properties=pika.BasicProperties(content_type='text/plain'),
                                  body='{"hostname":"%s"}' % hostname)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(thread_function, queue='vnfm.%s.actions' % hostname)
            channel.start_consuming()
        except Exception:
            # logging.exception('')
            time.sleep(sleep_time)
            if (sleep_time < 10):
                sleep_time = sleep_time + 1
            else:
                sleep_time = sleep_time + 10
            #print("Trying to reconnect")
            # log.info("Trying to reconnect...")
