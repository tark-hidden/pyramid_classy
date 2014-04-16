Pyramid-Classy
==============

.. module:: pyramid_classy

Pyramid-Classy is an extension that adds class-based views to Pyramid.
FOR PRETTY COMMON CASES.

For example, `Pyramid-Classy` will automatically generate routes based on the methods
in your views, and makes it super simple to override those routes
using Flask's familiar decorator syntax.

Installation
------------

Install the extension with::

    $ pip install pyramid-classy

or
    
    $ easy_install pyramid-classy

A standard way URL-Dispatch Pyramid
-----------------------------------

::

import random
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

quotes = [
    "First quote",
    "Second quote",
    "Third quote",
    "Fourth quote",
]

class IndexView(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name='index',
                 renderer='classy_test:/templates/mytemplate.pt')
    def index(self):
        return {'quotes': quotes}

    @view_config(route_name='index.random')
    def random(self):
        return Response(random.choice(quotes))

    @view_config(route_name='index.get')
    def get(self):
        quote_id = int(self.request.matchdict['id'])
        quote = quotes[quote_id if 0 < quote_id < len(quotes) else 0]
        return Response(quote)


class SecondView(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name='second.index')
    def index(self):
        return Response('Second View index')

    @view_config(route_name='second.random')
    def random(self):
        return Response(random.choice(quotes))


def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.add_route('index', '/')
    config.add_route('index.random', '/random')
    config.add_route('index.get', '/{id:\d+}')
    config.add_route('second.index', '/second/')
    config.add_route('second.random', '/second/random')
    config.scan()

    return config.make_wsgi_app()

Sure enough, it is an useless example. You need to define routes and views.
It seems like Django + Bottle in one framework.

What do you think about this?
-----------------------------

import random

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import notfound_view_config
from classy_test.pyramid_classy import ClassyView, route


quotes = [
    "First quote",
    "Second quote",
    "Third quote",
    "Fourth quote",
]


class IndexView(ClassyView):
    @route('/', renderer='classy_test:/templates/mytemplate.pt')
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


What do you think? Amazing, isn't it? More simple than standard way!


Customizing the Route Base
~~~~~~~~~~~~~~~~~~~~~~~~~~
There are 2 ways to customize the base route of a `FlaskView`. (Well
technically there are 3 if you count changing the name of the class
but that's hardly a reasonable way to go about it.)

Method 1:
*********

The first method simply requires you to set a `route_base` attribute on
your `FlaskView`. Suppose we wanted to make our QuotesView handle the
root of the web application::

    class IndexView(ClassyView):
        route_base = '/'

        def index(self):
            ...

        def get(self, id):
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What happens when you need to apply more than one route to a specific view. 
But since you're so determined let's see how to do that anyway.

So let's say you add the following routes to one of your views::

    class IndexView(ClassyView):
        route_base = '/'

        @route('/{id:\d+}')
        @route('/quote-{id:\d+}')
        def get(self, id):
            ...

That would end up generating the following 2 routes: /<id> and /quote-<id>
route_name would be index.get_0 and index.get_1


Special names
-------------

Classnames IndexView or Index will always use / as route_base.
Method named index(self, request) will always use /<class_name>/ for route_path.

Classnames will always use /<class_name>/ as route_base if you don't define route_base in class.
Methods without decorators will use /<class_name>/<method_name> for route_path.

The route decorator takes exactly the same parameters as Pyramid's add_router, 
so you should feel right at home adding custom routes to any views you create.
