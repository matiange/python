# -*- coding: utf-8 -*-
import setuptools
import simple_http_server

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple_http_server",
    version=simple_http_server.version,
    author="MaTianGe",
    author_email="matiange2012@163.com",
    description="爬取特种加工作业证书信息的服务",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matiange/python.git",
    include_package_data=True,
    packages=["simple_http_server"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
