Pyramid-Classy
==============
Translation and bug fix in progress.

I like Flask. Almost all of my projects are just a combination of Flask, Flask-Classy and Flask-Admin.
But now I have decided to try my hand at Pyramid.

Pyramid-Classy is an extension that allows implementing several commonly used features.
The main idea was taken from the Flask-Classy written by Freedom Dumlao, god bless him.

For example, Pyramid-Classy will automatically generate routes based on the methods in your views,
at the same time providing a simple way to override those routes using Pyramid's familiar decorator

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
    from pyramid.response import Response
    from pyramid_classy import ClassyView, route


    quotes = [
        "First quote",
        "Second quote",
        "Third quote",
        "Fourth quote",
    ]

    @view_defaults(renderer='project:/templates/single.pt')
    class IndexView(ClassyView):
        @route('/')
        def index(self, renderer='project:/templates/index.pt'):  # /
            return dict(quotes=quotes)

        def random(self):  # /random
            return dict(quote=random.choice(quotes))

        @route('/{id:\d+}')
        @route('/quote-{id:\d+}')
        def get(self):  # /1 and /quote-1
            quote_id = int(self.request.matchdict['id'])
            quote = quotes[quote_id if 0 < quote_id < len(quotes) else 0]
            return dict(quote=quote)


    class SecondView(ClassyView):
        def index(self):  # /second/
            return Response('Second View index')

        def random(self):  # /second/random
            return Response(random.choice(quotes))


    def main(global_config, **settings):
        config = Configurator(settings=settings)

        IndexView.register(config, debug=True)
        SecondView.register(config)

        return config.make_wsgi_app()


Amazing, isn't it? Write less, do more.


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

Classnames IndexView or Index will always use / as route_base.
Method named index(self, request) will always use /<class_name>/ for route_path.

Classnames will always use /<class_name>/ as route_base if you don't define route_base in class.
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
Sure enough, you cannot handle URLs with name starting with underscore. Sorry for that.

.. code-block:: python

    class IndexView(ClassyView):
        debug = True
        
        def _get_some_info(self):  # /_get_some_info (!) -> 404 (Not Found)
            return something


Last words
----------

Ah. I have read the article http://me.veekun.com/blog/2011/07/14/pyramid-traversal-almost-useful/

.. code-block:: python

    config.add_route('cats.list', '/cats')
    config.add_route('cats.view', '/cats/{id:\d+}', pregenerator=make_cat_url)
    config.add_route('cats.owners', '/cats/{id:\d+}/owners', pregenerator=make_cat_url)
    config.add_route('cats.shots', '/cats/{id:\d+}/shots', pregenerator=make_cat_url)
    config.add_route('cats.youtubes', '/cats/{id:\d+}/youtubes', pregenerator=make_cat_url)
    config.add_route('cats.hurpdurp', '/cats/{id:\d+}/hurpdurp', pregenerator=make_cat_url)
    config.add_route('dogs.view', '/dogs/{id:\d+}', pregenerator=make_dog_url)
    config.add_route('dogs.owners', '/dogs/{id:\d+}/owners', pregenerator=make_dog_url)
    config.add_route('dogs.shots', '/dogs/{id:\d+}/shots', pregenerator=make_dog_url)
    config.add_route('dogs.youtubes', '/dogs/{id:\d+}/youtubes', pregenerator=make_dog_url)
    config.add_route('dogs.hurpdurp', '/dogs/{id:\d+}/hurpdurp', pregenerator=make_dog_url)

This is really sad. What about this?

.. code-block:: python

    class PetView(ClassyView):
        def __init__(self, request):
            super(PetView, self).__init__(request)
            self.pet_class = request.path.split('/')[1]

        @route('/', renderer='...')
        def list(self):  # /
            pet_class = self.pet_class
            return ...

        @route('/{id:\d+}', renderer='...')
        def view(self):  # /232
            pet_class = self.pet_class
            return ...

        @route('/{id:\d+}/owners', renderer='...')
        def owners(self):  # /232/owners
            pet_class = self.pet_class
            return ...

        @route('/{id:\d+}/shots', renderer='...')
        def shots(self):  # /232/shots
            pet_class = self.pet_class
            return ...

        @route('/{id:\d+}/youtubes', renderer='...')
        def youtubes(self):  # /232/youtubes
            pet_class = self.pet_class
            return ...

        @route('/{id:\d+}/hurpdurp', renderer='...')
        def hurpdurp(self):  # /232/hurpdurp
            pet_class = self.pet_class
            return ...

    ...

    def main(global_config, **settings):
        config = Configurator(settings=settings)

        PetView.register(config, '/cats')
        PetView.register(config, '/dogs')

        return config.make_wsgi_app()


You're welcome, bro.

Changelog
*********

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
