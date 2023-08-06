# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="baidumap",
    version="1.0.0",
    keywords=("baidu", "map", "api", "web"),
    description="api handle for baidu map",
    long_description='''
        an easy handle to call baidu map api, which will return object
    ''',
    license="MIT Licence",
    url="https://github.com/cpak00/baidumap",
    author="chenyiming",
    author_email="cymcpak00@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["requests"])
