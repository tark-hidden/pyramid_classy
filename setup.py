"""
Pyramid-Classy
-------------

Class-based views for Pyramid
"""
from setuptools import setup

setup(
    name='Pyramid-Classy',
    version='0.1',
    url='https://github.com/tark-hidden/pyramid-classy',
    license='BSD',
    author='Tark',
    author_email='tark.hidden@gmail.com',
    description='Class-based views for Pyramid',
    long_description=__doc__,
    py_modules=['pyramid_classy'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Pyramid'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]    
)
