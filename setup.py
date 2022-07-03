"""
Pyramid-Classy
--------------

Pyramid-Classy is an extension that adds class-based views to
Pyramid more simple. Main idea was taken from the Flask-Classy written by
Freedom Dumlao.

Documentation: https://github.com/tark-hidden/pyramid_classy

Changelog
*********

0.4.4
-----

* No more print if debug=True, now it depends on logging in a Pyramid config file.
* Fixed too long route_name if class view inherit other class.


0.4.2
-----

* Py3 compatibility support.


0.4
---

* IndexView is very useful name, but... Now you can handle a root url with any class you want - with route_base = '/'.
* Some weird bugs has been fixed.


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


requires = [
    'pyramid',
    'webtest',
    'waitress'
]


setup(
    name='pyramid-classy',
    version='0.4.4',
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
    test_suite="tests",
    tests_require=requires,
    install_requires=requires,
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]    
)
