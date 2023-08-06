# -*- coding: utf-8 -*-
"""
    Babel localisation support for aiohttp
    代码从 https://github.com/jie/aiohttp_babel 拷贝并修改
"""
from setuptools import setup
from setuptools import find_packages
import os

def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()

setup(
    name = "mw-aiohttp-babel",
    version = "0.1.3",
    packages = find_packages(),
    install_requires = [
        "aiohttp",
        "babel",
        "speaklater",
    ],
    author = "cxhjet",
    author_email = "cxhjet@qq.com",
    description = "Babel localisation support for aiohttp,适用maxwin团队的开发框架",
    long_description='\n\n'.join((read('README.rst'), read('CHANGES.txt'))),
    license = "BSD",
    keywords = "aiohttp locale babel localisation",
    url = "https://bitbucket.org/maxwin-inc/mw-aiohttp-babel/src",
)
