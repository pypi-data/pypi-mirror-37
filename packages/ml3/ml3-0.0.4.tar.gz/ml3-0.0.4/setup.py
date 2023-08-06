#!/usr/bin/env python
# 详细的setup.py参考：http://blog.konghy.cn/2018/04/29/setup-dot-py/
# 参考http://www.wbh-doc.com.s3.amazonaws.com/Python-with-GitHub-PyPI-and-Readthedoc-Guide/chapter1%20-%20setup.py%20file%20guide%20for%20human.html
# 上面的链接更加详细
import re


try:
    from setuptools import setup,find_packages
except ImportError:
    from distutils.core import setup


version = '0.0.4'

if not version:
    raise RuntimeError('Cannot find version information')


with open('README.rst', 'rb') as f:
    readme = f.read().decode('utf-8')
found_packages = find_packages(exclude=["doc","examples","test"])
#print(found_packages)
setup(
    name='ml3',
    author='Jiao Shuai',
    author_email='jiaoshuaihit@gmail.com',
    version=version,
    description='TechYoung Machine Learning ToolKit',
    long_description=readme,
    packages=found_packages,
    install_requires=['scikit-learn>=0.19.1'],
    include_package_data=True,
    url='http://ml3.techyoung.cn',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
