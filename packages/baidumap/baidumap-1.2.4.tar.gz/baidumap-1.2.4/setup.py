# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="baidumap",
    version="1.2.4",
    keywords=("baidu", "map", "api", "web"),
    description="api handle for baidu map",
    long_description=open('baidumap/README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license="MIT Licence",
    url="https://github.com/cpak00/baidumap",
    author="chenyiming",
    author_email="cymcpak00@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["requests"],
    data_files=['baidumap/README.md'])
