# encoding: utf-8

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_defaults
from pyramid_classy import ClassyView, route
from webtest import TestApp
import unittest
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


class ClassyTests(unittest.TestCase):
    def request_route_path(self, route_name):
        # dirty...
        return self.testapp.app.routes_mapper.routes[route_name].path

    def setUp(self):

        @view_defaults(renderer='string')
        class IndexView(ClassyView):
            @route('/')
            def index(self):
                return 'Index page'

            @route('/about')
            def about(self):
                return 'About page'

        @view_defaults(renderer='string')
        class NewsView(ClassyView):
            @route('/')
            def index(self):  # /news/
                return 'Top news'

            @route('/{year:\d+}')
            def year(self):  # /news/year
                year = self.request.matchdict['year']
                return 'Top news stories of %s year' % year

            @route('/{year:\d+}/{month:\d+}')
            def month(self):  # /news/year/month
                year = self.request.matchdict['year']
                month = self.request.matchdict['month']
                return 'Top news stories of %s year %s month' % (month, year)

            @route('/{year:\d+}/{month:\d+}/{day:\d+}')
            def day(self):  # /news/year/month/day
                year = self.request.matchdict['year']
                month = self.request.matchdict['month']
                day = self.request.matchdict['day']
                return 'News of %s.%s.%s date' % (day, month, year)

        class ShopView(ClassyView):
            @route('/', renderer='string')
            def index(self):
                return 'Shop'

            @route('/order', route_name='money-money-money',
                   request_method=('GET', 'POST'), renderer='string')
            def order(self):
                return 'Goods order'

            @route('/{id:\d+}', renderer='string')
            def item(self):
                return 'Goods item'

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

        class CreditsView(ClassyView):
            """ It is very weird, but who knows...
                Don't forget: prefixes for route names will depends on original
                class name, i.e. credits.about and credits.index.
            """
            route_base = '/company/'

            @route('/', renderer='string')
            def index(self):
                return 'Credits page with route_base inside class'

            def about(self):
                return Response('About our company and partners '
                                'without decorator. URL is /company/about here')

        def main(global_config, **settings):
            config = Configurator(settings=settings)

            IndexView.register(config)
            NewsView.register(config)
            ShopView.register(config, route_base='/goods/')
            AnimalView.register(config)
            DogView.register(config, route_base='/dog/')
            CreditsView.register(config)

            return config.make_wsgi_app()

        settings = {}
        app = main({}, **settings)
        self.testapp = TestApp(app)

    def tearDown(self):
        pass

    def test_root(self):
        res = self.testapp.get('/')
        self.assertTrue(b'Index page' in res.body)

    def test_root_about(self):
        res = self.testapp.get('/about', status=200)
        self.assertTrue(b'About' in res.body)

    def test_news_year(self):
        res = self.testapp.get('/news/2016', status=200)
        self.assertTrue(b'Top news stories of 2016 year' in res.body)

    def test_inherit_view(self):
        res = self.testapp.get('/dog/add', status=200)
        self.assertTrue(b'species' in res.body)

    def test_internal_route_base(self):
        res = self.testapp.get('/company/', status=200)
        self.assertTrue(b'with route_base inside class' in res.body)

    def test_undecorated_view(self):
        res = self.testapp.get('/company/about', status=200)
        self.assertTrue(b'company and partners' in res.body)

    def test_404(self):
        res = self.testapp.get('/some/news', status=404)
        self.assertTrue(b'Not Found' in res.body)

        res = self.testapp.get('/news/201b/', status=404)
        self.assertTrue(b'Not Found' in res.body)

        res = self.testapp.put('/goods/order', status=404)
        self.assertTrue(b'Not Found' in res.body)

    def test_route_names(self):
        res = self.testapp.get(self.request_route_path('money-money-money'),
                               status=200)
        self.assertTrue(b'Goods order' in res.body)
        self.assertTrue(res.request.environ['PATH_INFO'] == '/goods/order')

        res = self.testapp.get(self.request_route_path('dog.add'),
                               status=200)
        self.assertTrue(b'UI for appending some species' in res.body)
        self.assertTrue(res.request.environ['PATH_INFO'] == '/dog/add')

        res = self.testapp.get(self.request_route_path('dog.index'),
                               status=200)
        self.assertTrue(b'Dog' in res.body)
        self.assertTrue(res.request.environ['PATH_INFO'] == '/dog/')

        res = self.testapp.get(self.request_route_path('shop.goods.index'),
                               status=200)
        self.assertTrue(b'Shop' in res.body)
        self.assertTrue(res.request.environ['PATH_INFO'] == '/goods/')
