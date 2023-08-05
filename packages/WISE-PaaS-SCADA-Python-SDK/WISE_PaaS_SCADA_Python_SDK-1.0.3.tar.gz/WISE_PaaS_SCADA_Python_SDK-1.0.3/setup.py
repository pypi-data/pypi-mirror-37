import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WISE_PaaS_SCADA_Python_SDK",
    version="1.0.3",
    author="Stacy Yeh",
    author_email="stacy.yeh@advantech.com",
    description="The WISEPaaS_SCADA_Python_SDK package allows developers to write Python applications which access the WISE-PaaS Platform via MQTT or MQTT over the Secure WebSocket Protocol.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/advwacloud/WISEPaaS.SCADA.Python.SDK",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)