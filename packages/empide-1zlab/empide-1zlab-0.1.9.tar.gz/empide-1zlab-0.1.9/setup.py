import os
from setuptools import find_packages, setup




setup(
    name='empide-1zlab',
    version='0.1.9',
    packages=['ide'],
    include_package_data=True,
    license='MIT License',
    description='maybe the best develop tools for micropython.',
    url='http://emp.1zlab.com/',
    author='Fuermohao',
    author_email='Fuermohao@outlook.com',
    platforms='Linux,Unix',
    keywords='MicroPython,1ZLAB,EMP,ESP',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
