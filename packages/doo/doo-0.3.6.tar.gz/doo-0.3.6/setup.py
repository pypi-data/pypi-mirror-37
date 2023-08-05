from setuptools import setup, find_packages


setup(
    name="doo",
    version="0.3.6",
    author="Leo Tong",
    author_email="tonglei@qq.com",
    description="doo",
    long_description=open("README.rst").read(),
    license="Apache License, Version 2.0",
    url="https://github.com/tonglei100/xiaomi",
    packages=['doo'],
    package_data={'doo': ['*.py', '*.xlsx', '*.json', '*.yml']},
    install_requires=[
        'xlrd',
        'xlsxwriter',
        'apistar<0.6.0'
        ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3"
    ],
    entry_points={
        'console_scripts': [
            'doo=doo:doo'
        ]    

    }
)
