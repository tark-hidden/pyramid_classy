# encoding: utf-8
"""
    It is port from Flask-Classy, you know.
"""

import inspect

temp_rule_cache = None


def route(rule, **options):
    def decorator(f):
        global temp_rule_cache
        if temp_rule_cache is None:
            temp_rule_cache = {f.__name__: [(rule, options)]}
        elif not f.__name__ in temp_rule_cache:
            temp_rule_cache[f.__name__] = [(rule, options)]
        else:
            temp_rule_cache[f.__name__].append((rule, options))
        return f
    return decorator


def get_members(base, current):
    base_members = dir(base)
    all_members = inspect.getmembers(current, predicate=inspect.ismethod)
    return [member for member in all_members
            if not member[0] in base_members and not member[0].startswith('_')]


class ClassyViewMeta(type):
    def __init__(cls, name, bases, dct):
        global temp_rule_cache
        super(type, cls).__init__()
        if temp_rule_cache:
            cls.rule_cache = temp_rule_cache
            temp_rule_cache = None


ClassyViewBase = ClassyViewMeta('_ClassyViewBase', (object, ), {})


class ClassyView(ClassyViewBase):
    route_base = '/'
    cls_name = ''
    decorators = []

    @classmethod
    def register(cls, config, route_base=None):
        cn = cls.__name__
        cls.cls_name = (cn[:-4] if len(cn) > 4 and cn.endswith("View")
                        else cn).lower()
        if route_base:
            cls.route_base = route_base
        if cls.route_base == '/' or not cls.route_base:
            cls.route_base = '' if cls.cls_name == 'index' \
                else '/' + cls.cls_name.strip('/')

        for name, function in get_members(ClassyView, cls):
            function = cls.make_proxy_method(name)
            if hasattr(cls, "rule_cache") and name in cls.rule_cache:
                for idx, rule in enumerate(cls.rule_cache[name]):
                    url, options = rule
                    url = cls.build_url(name, url)
                    route_name, options = cls.parse_options(options)

                    if not route_name:
                        route_name = cls.build_endpoint(name)
                    if len(cls.rule_cache[name]) > 1:
                        route_name = '%s_%d' % (route_name, idx)

                    config.add_route(route_name, url)
                    config.add_view(function, route_name=route_name, **options)
            else:  # no decorators
                url = cls.build_url(name, name)
                route_name = cls.build_endpoint(name)
                config.add_route(route_name, url)
                config.add_view(function, route_name=route_name)

    @classmethod
    def parse_options(cls, options):
        return options.pop('route_name', None), options

    @classmethod
    def build_endpoint(cls, method):
        return '%s.%s' % (cls.cls_name, method)

    @classmethod
    def build_url(cls, name, url=''):
        if name == 'index':
            url = ''
        return '%s/%s' % (cls.route_base, url.lstrip('/'))

    @classmethod
    def make_proxy_method(cls, name):
        view = getattr(cls(), name)

        if cls.decorators:
            for decorator in cls.decorators:
                view = decorator(view)
        return view
