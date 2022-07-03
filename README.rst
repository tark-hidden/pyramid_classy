Pyramid-Classy
==============
Translation and bug fix in progress.

Pyramid-Classy is an extension that allows implementing several commonly used features.
The idea was taken from the Flask-Classy written by Freedom Dumlao.

Pyramid-Classy will automatically generate routes based on the methods
in your views, at the same time providing a simple way to override those routes
using Pyramid's familiar decorator.

Installation
------------

Install the extension with::

    $ pip install pyramid-classy

or::

    $ easy_install pyramid-classy


Let's see how it works
----------------------

.. code-block:: python

    import random
    from pyramid.config import Configurator
    from pyramid_classy import ClassyView, route


    quotes = [
        "First quote",
        "Second quote",
        "Third quote",
        "Fourth quote",
    ]

    @view_defaults(renderer='/single.jinja2')
    class IndexView(ClassyView):
        @route('/', renderer='/index.jinja2')
        def index(self):  # /
            return dict(quotes=quotes)

        def random(self):  # /random
            return dict(quote=random.choice(quotes))

        @route('/{id:\d+}')
        @route('/quote-{id:\d+}')
        def get(self):  # /1 and /quote-1
            quote_id = int(self.request.matchdict['id'])
            quote = quotes[quote_id if 0 < quote_id < len(quotes) else 0]
            return dict(quote=quote)


    class UserView(ClassyView):
        @route('/')
        def index(self):  # /user/
            return HTTPNotFound()

        @route('/login', renderer='/user/login.jinja2')
        def login(self):  # /user/login
            request = self.request
            if request.method == 'POST':
                return ...
            return {}

        @route('/register', renderer='/user/register.jinja2')
        def register(self):  # /user/register
            request = self.request
            if request.method == 'POST':
                return ...
            return {}


    def main(global_config, **settings):
        config = Configurator(settings=settings)

        IndexView.register(config)
        UserView.register(config)

        """ Instead of something like:

        config.add_route('index', '/')
        config.add_route('random', '/random')
        config.add_route('get_1', '/{id:\d+}')
        config.add_route('get_2', '/quote-{id:\d+}')
        config.add_route('user', '/user')
        config.add_route('user_login', '/user/login')
        config.add_route('user_register', '/user/register')
        config.scan()
        """

        return config.make_wsgi_app()


Customizing the Route Base
--------------------------
There are two ways to customize the base route of a `ClassyView`. Well,
technically there are three if you count changing the name of the class
but that's hardly a reasonable way to go about it.

Method 1:
*********

The first method simply requires you to set a `route_base` attribute on
your `ClassyView`. Suppose we wanted to make our QuotesView handle the
root of the web application

.. code-block:: python

    class QuotesView(ClassyView):
        route_base = '/'

        def index(self):
            ...

        def get(self):
            ...


Method 2:
*********

The second method is perfect for when you're using app factories, and
you need to be able to specify different base routes for different apps.
You can specify the route when you register the class with the Pyramid config
instance::

    QuotesView.register(config, route_base='/')


The second method will always override the first, so you can use method
one, and override it with method two if needed.


Using multiple routes for a single view
---------------------------------------

Sometimes you need to apply more than one route to a specific view...

.. code-block:: python

    class IndexView(ClassyView):
        route_base = '/'

        @route('/{id:\d+}')
        @route('/quote-{id:\d+}')
        def get(self):
            ...

That would end up generating the following 2 routes: /<id> and /quote-<id>
route_name would be index.get_1 and index.get_0


Important notes
---------------

It was written in Python 3.3 (and checked with Python 2.7) for Pyramid 1.7.3.

Classnames IndexView or Index will always use / as route_base.

Classnames will always use /<class_name>/ as route_base if you don't define route_base in class or the class is not inherit other class.
Methods without decorators will use /<class_name>/<method_name> for route_path.

The route decorator takes exactly the same parameters as Pyramid's add_route,
so you should feel free adding custom routes to any views you create.

You can define debug flag (same way as route_base) to see routes and endpoints.

All the functions with name starting with letter and defined in class ClassyView will 
serve a specified URL even without route decorator.

.. code-block:: python

    class IndexView(ClassyView):
        debug = True
        
        def get_some_info(self):  # /get_some_info (!) -> 502 (Server Error)
            return something

For avoiding this you need to define a function with name starting with underscore _.
Yes, you cannot handle URLs with name starting with underscore. Sorry for that.

.. code-block:: python

    class IndexView(ClassyView):
        debug = True
        
        def _get_some_info(self):  # /_get_some_info (!) -> 404 (Not Found)
            return something


Known issues
------------

.. code-block:: python

    class AnimalView(ClassyView):
        @route('/', renderer='string')
        def index(self):
            return 'Animal'

        @route('/add', renderer='string')
        def add(self):
            return 'UI for appending some species'

    class DogView(AnimalView):
        @route('/', renderer='string')
        def index(self):
            return 'Dog inherit animal'


    AnimalView.register(config)
    DogView.register(config)


Because of AnimalView has a self route_base after register and DogView is
inheritance of AnimalView, then DogView route_base will be defined as
'/animal' without overriding. Be careful.


Pitfalls
--------

.. code-block:: python

    class AboutUsView(ClassyView)
        route_base = '/about'

        @route('/')
        def index(self):
            return HTTPNotFound()

        @route('/company', ...)
        def company(self):
            return {}


Here is route_name values will depends on original class name; first one will be
'aboutus.index' which will handle '/about' URL, and second one will
be 'aboutus.company' -> '/about/company' URL.

Well... debug=True is a good way to avoid it.


Changelog
*********

0.4.4
~~~~~

* No more print if debug=True, now it depends on logging in a Pyramid config file.
* Fixed too long route_name if class view inherit other class.


0.4.2
~~~~~

* Py3 compatibility support.


0.4
~~~

* IndexView is very useful name, but... Now you can handle the root url with any class you want - with route_base = '/'.
* Some weird bugs has been fixed.


0.3
~~~

* Fixed a terrible bug, that doesn't allow to define a few routes for the root.
* Added debug flag. Now you can see routes and their names if you want.
* Added @view_defaults support. It's weird, but it didn't work properly.


0.2
~~~

* Cleaned up code.
* Now functions in classes accepts only one argument: self. Request variable now is self.request.


0.1
~~~

Initial release.
