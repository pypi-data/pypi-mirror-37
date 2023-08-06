# coding: utf-8

"""
    Omnichannel API

    Messente's API which allows sending messages via various channels with fallback options.  # noqa: E501

    OpenAPI spec version: 0.0.2
    Contact: admin@messente.com
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "omnichannel-api"
VERSION = "0.0.2"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="Omnichannel API",
    author_email="admin@messente.com",
    url="https://messente.com/documentation",
    keywords=["omnichannel", "sms", "viber"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    Messente&#39;s API which allows sending messages via various channels with fallback options.  # noqa: E501
    """
)
