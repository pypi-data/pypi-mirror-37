import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mc_coppel",
    version="4.0.3",
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
    'simplejson',
    'pymongo',
    'kafka',
    'requests',
    'aiokafka',
    'uuid',
    'colorama',
    'mongoengine',
    'geopy',
    'jsonmerge']
)