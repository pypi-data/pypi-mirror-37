# -*- coding: utf-8 -*-
"""setup script

"""
import io
import re
import setuptools


with open('README.md', 'r') as fh:
    readme = fh.read()

with io.open('monitor_register/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setuptools.setup(
    name='monitor_register',
    author='stsean',
    author_email="author@example.com",
    version=version,
    description='Register to monitor server',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='http://git.azure.gagogroup.cn/huangtaihu/python-log-register.git',
    packages=[
        'monitor_register',
        'monitor_register/api_doc',
        'monitor_register/monitor',
        'monitor_register/util',
    ],
    python_requires='>3.6.0',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[]
)
