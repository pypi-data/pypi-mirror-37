from setuptools import setup

setup(
    name='json2simplejson',
    version='1.0.0',
    packages=['json2simplejson'],
    url='https://jakegealer.me',
    license='GPL-3.0',
    author='Jake Gealer',
    install_requires=["simplejson"],
    author_email='jake@gealer.email',
    description='A simple monkey patcher in order to make things that run using the standard "json" library (such as discord.py) use the quicker "simplejson" library.'
)
