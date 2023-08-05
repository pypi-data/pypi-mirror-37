#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

long_description = """
操作更方便的xpath

使用方法类似于Beautiful Soup4, 但是比他更快速

import zxpath

zx = zxpath.load('etree对象或者html源码') #加载

find() #查询一个节点, 失败返回None
zx.find('div', class_='content') #参考 .//div[@class="content"][1]
zx.find('div', class_=False) #参考 .//div[not(@class)][1]
zx.find('div', _class_='content') #参考 .//div[not(@class="content")][1]
zx.find('div', class=True, sun_node=False) #参考 ./div[@class][1] sun_node表示是否递归查询孙级节点

find_all() # 查询多个节点, 参数同find, 返回一个列表, 失败返回空列表
zx(*attr, **kw) #同find_all

#_Element对象
node = zx.find('div')

node.id #获取id属性
node.text #获取文本
node.string #获取整个div的所有文本
node.a #获取在这个节点下搜索到的第一个a元素节点
node.html #获取这个节点的html源码
node.find
node.find_all
node(*attr, **kw) #同find_all
node.xpath_one #使用原始xpath代码查询一个节点
node.xpath_all #使用原始xpath代码查询多个节点

更新日志:
1.0.1
    修复了一些bug, 该bug曾导致:
        在查找上一个同级节点时会忽略掉同级的文本节点
        在查找下一个同级节点时会忽略掉同级的文本节点
"""
setup(
    name='zxpath',
    version='1.0.1',
    py_modules=['zxpath'],
    author='zlyuan',
    author_email='1277260932@qq.com',
    packages=find_packages(),
    description='操作更方便的xpath, 使用方法类似于Beautiful Soup4, 但是比他更快速',
    long_description=long_description,  # 项目介绍
    url='https://pypi.org/',
    license='GNU GENERAL PUBLIC LICENSE',
    platforms=['all'],
    scripts=[],  # 额外的文件
    install_requires=['lxml'],  # 依赖库
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ]
)
