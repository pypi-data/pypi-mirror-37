import os


from setuptools import setup
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="alisoam-openbaton-ems",
    version="1.1.3rc5",
    author="Openbaton",
    author_email="ali.sorouramini@gmail.com",
    description="Openbaton generic EMS",
    license="Apache 2.0",
    keywords="python ems vnfm openbaton open baton",
    url="https://github.com/AliSoAm/ems",
    packages=["ems"],
    install_requires= ["pika", "gitpython", "pyyaml"],
    long_description="management system that works in conjuction with Openbaton Generic-VNFM",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: Apache Software License"
    ],
    scripts = ["add-upstart-ems"],
    entry_points={
        'console_scripts': [
            'openbaton-ems = ems.ems:main'
        ]
    },
)
