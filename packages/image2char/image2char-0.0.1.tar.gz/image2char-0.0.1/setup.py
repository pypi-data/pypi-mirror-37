# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

filepath = 'image2char/README.md'

setup(
    name="image2char",
    version="0.0.1",
    keywords=("image", "char", "transfer", "cmd", "shell"),
    description="small tool to transfer image between cmd char",
    long_description=open(filepath, encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license="MIT Licence",
    url="https://github.com/cpak00/charimage",
    author="cpak00",
    author_email="cymcpak00@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["pillow"],
    data_files=[filepath])
