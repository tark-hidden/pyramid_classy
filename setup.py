"""
Pyramid-Classy
--------------

Pyramid-Classy is an extension that adds class-based views to
Pyramid more simple. Main idea was taken from the Flask-Classy written by
Freedom Dumlao.

Documentation: https://github.com/tark-hidden/pyramid_classy

Changelog
*********

0.3
---

* Fixed a terrible bug, that doesn't allow to define a few routes for the root.
* Added debug flag. Now you can see routes and their names if you want.
* Added @view_defaults support. It's weird, but it didn't work properly.

        
0.2
---
        
* Cleaned up code. 
* Now functions in classes accepts only one argument: self. Request variable now is self.request.


0.1
---

Initial release.

"""
from setuptools import setup

setup(
    name='Pyramid-Classy',
    version='0.3',
    url='https://github.com/tark-hidden/pyramid_classy',
    license='BSD',
    author='Tark',
    maintainer="Tark",
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
