Pyramid-Classy
==============
The PyPi package is not ready yet.

I like Flask. Almost all of my projects are just a combination of Flask, Flask-Classy and Flask-Admin.
But now I have decided to try my hand at Pyramid.

Pyramid-Classy is an extension that allows implementing several commonly used features.
The main idea was taken from the Flask-Classy written by Freedom Dumlao, god bless him.

For example, `Pyramid-Classy` will automatically generate routes based on the methods
in your views, and makes it super simple to override those routes
using Pyramid's familiar decorator syntax.

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


    class IndexView(ClassyView):
        @route('/', renderer='app:/templates/mytemplate.pt')
        def index(self, request):  # /
            return {'quotes': quotes}

        def random(self, request):  # /random
            return Response(random.choice(quotes))

        @route('/{id:\d+}')
        @route('/quote-{id:\d+}')
        def get(self, request):  # /1 and /quote-1
            quote_id = int(request.matchdict['id'])
            quote = quotes[quote_id if 0 < quote_id < len(quotes) else 0]
            return Response(quote)


    class SecondView(ClassyView):
        def index(self, request):  # /second/
            return Response('Second View index')

        def random(self, request):  # /second/random
            return Response(random.choice(quotes))


    def main(global_config, **settings):
        config = Configurator(settings=settings)

        IndexView.register(config)
        SecondView.register(config)

        return config.make_wsgi_app()


What do you think? Amazing, isn't it? Write less do more.


Customizing the Route Base
--------------------------
There are 2 ways to customize the base route of a `ClassyView`. (Well
technically there are 3 if you count changing the name of the class
but that's hardly a reasonable way to go about it.)

Method 1:
*********

The first method simply requires you to set a `route_base` attribute on
your `ClassyView`. Suppose we wanted to make our QuotesView handle the
root of the web application

.. code-block:: python

    class IndexView(ClassyView):
        route_base = '/'

        def index(self, request):
            ...

        def get(self, request):
            ...


Method 2:
*********

The second method is perfect for when you're using app factories, and
you need to be able to specify different base routes for different apps.
You can specify the route when you register the class with the Pyramid config
instance::

    IndexView.register(config, route_base='/')

The second method will always override the first, so you can use method
one, and override it with method two if needed.


Using multiple routes for a single view
---------------------------------------

What happens when you need to apply more than one route to a specific view.
But since you're so determined let's see how to do that anyway.

So let's say you add the following routes to one of your views

.. code-block:: python

    class IndexView(ClassyView):
        route_base = '/'

        @route('/{id:\d+}')
        @route('/quote-{id:\d+}')
        def get(self, request):
            ...

That would end up generating the following 2 routes: /<id> and /quote-<id>
route_name would be index.get_1 and index.get_0


Special names
-------------

Classnames IndexView or Index will always use / as route_base.
..Method named index(self, request) will always use /<class_name>/ for route_path.

Classnames will always use /<class_name>/ as route_base if you don't define route_base in class.
..Methods without decorators will use /<class_name>/<method_name> for route_path.

The route decorator takes exactly the same parameters as Pyramid's add_router,
so you should feel right at home adding custom routes to any views you create.

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
        def _pet_class(self, request):
            return request.path.split('/')[1]

        @route('/', renderer='...')
        def list(self, request):  # /
            pet_class = self._pet_class(request)
            return ...

        @route('/{id:\d+}', renderer='...')
        def view(self, request):  # /232
            pet_class = self._pet_class(request)
            return ...

        @route('/{id:\d+}/owners', renderer='...')
        def owners(self, request):  # /232/owners
            pet_class = self._pet_class(request)
            return ...

        @route('/{id:\d+}/shots', renderer='...')
        def shots(self, request):  # /232/shots
            pet_class = self._pet_class(request)
            return ...

        @route('/{id:\d+}/youtubes', renderer='...')
        def youtubes(self, request):  # /232/youtubes
            pet_class = self._pet_class(request)
            return ...

        @route('/{id:\d+}/hurpdurp', renderer='...')
        def hurpdurp(self, request):  # /232/hurpdurp
            pet_class = self._pet_class(request)
            return ...

    ...

    def main(global_config, **settings):
        config = Configurator(settings=settings)

        PetView.register(config, '/cats')
        PetView.register(config, '/gods')

        return config.make_wsgi_app()


You're welcome, bro.
