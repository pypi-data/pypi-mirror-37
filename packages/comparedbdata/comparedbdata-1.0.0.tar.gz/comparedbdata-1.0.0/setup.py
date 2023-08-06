"""
File: setup.py.py
Created by: 陈辰柄 
Time: 2018/10/31 17:45
"""
from setuptools import setup,find_packages

setup(
    name='comparedbdata',
    version='1.0.0',
    description="数据对比程序",
    author='陈辰柄',
    # py_modules=['login_update_release_version'],
    author_email='375285942@qq.com',
    packages = find_packages(),
    exclude_package_date={'':['.gitignore','.pytest_cache']},
    platforms=["all"],
    include_package_data=True,
    install_requires=['PyMySQL>=0.9.2',
                      'pymongo>=3.7.1',
                      'pytest>=3.8.1',
                      'pytest-html>=1.19.0',
                      'pytest-xdist>=1.23.2',
                      ]
)