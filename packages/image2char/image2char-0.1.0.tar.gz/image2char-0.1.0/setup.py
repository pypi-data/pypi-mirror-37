# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

filepath = './image2char/README.md'

setup(
    name="image2char",
    version="0.1.0",
    keywords=("image", "char", "transfer", "cmd", "shell"),
    description="small tool to transfer image between cmd char",
    long_description=open(filepath, encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license="MIT Licence",
    url="https://github.com/cpak00/image2char",
    author="cpak00",
    author_email="cymcpak00@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    scripts=['./image2char.py'],
    install_requires=["pillow", "requests"],
    data_files=[filepath, './image2char/input1.jpg'])

print('welcome to use image2char module\nauthor: cpak00')
image2char = __import__('image2char.run')
run = image2char.run
run.main()
