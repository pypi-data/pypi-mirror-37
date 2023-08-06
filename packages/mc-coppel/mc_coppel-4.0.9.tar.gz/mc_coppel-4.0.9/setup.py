import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mc_coppel",
    version="4.0.9",
    author="Sergio Jimenez",
    author_email="menine77@gmail.com",
    description="libreria para hacer la conexion de microservicios",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires=[
    'simplejson==3.16.0',
    'pymongo==3.7.2',
    'kafka==1.3.5',
    'requests==2.20.0',
    'aiokafka==0.4.2',
    'uuid==1.30',
    'colorama==0.4.0',
    'mongoengine==0.15.3',
    'geopy==1.17.0',
    'jsonmerge==1.5.1']
)