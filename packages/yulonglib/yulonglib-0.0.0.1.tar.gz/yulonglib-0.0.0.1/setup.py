# coding:utf-8

from setuptools import setup

setup(
    name='yulonglib',     # 包名字
    version='0.0.0.1',   # 包版本
    description='功能齐全的jseq工具;功能齐全的conf工具;sock工具;多进线程工具',   # 简单描述
    author='pydison',  # 作者
    author_email='pydison@gmail.com',  # 作者邮箱
    url='http://pydison.github.io',      # 包的主页
    packages=['yulonglib',],                 # 包
    install_requires=['requests>=1.0',],
)
