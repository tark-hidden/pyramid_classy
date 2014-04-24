# encoding: utf-8
"""
    Pyramid-Classy is an extension that adds class-based views to
    Pyramid more simple.
"""

import inspect


def route(rule, **options):
    def decorator(f):
        if not hasattr(f, 'rules'):
            f.rules = []
        f.rules.append((rule, options))
        return f
    return decorator


def get_members(base, current):
    base_members = dir(base)
    all_members = inspect.getmembers(current, predicate=inspect.ismethod)
    return [member for member in all_members
            if not member[0] in base_members and not member[0].startswith('_')]


class ClassyView(object):
    route_base = '/'
    decorators = []

    @classmethod
    def register(cls, config, route_base=None):
        n = cls.__name__
        prefix = (n[:-4] if len(n) > 4 and n.endswith('View') else n).lower()
        if route_base and route_base != '/':
            cls.route_base = '/%s' % route_base.strip('/')
            prefix = '%s.%s' % (prefix, route_base.strip('/'))
        if cls.route_base == '/':
            cls.route_base = '' if prefix == 'index' else '/%s' % prefix

        for name, _ in get_members(ClassyView, cls):
            function = cls.make_proxy_method(name)
            if hasattr(getattr(cls, name), 'rules'):
                rules = getattr(cls, name).rules
                for idx, rule in enumerate(rules):
                    url, options = rule
                    url = cls.build_url(name, url)
                    route_name = options.pop('route_name', None)

                    if not route_name:
                        route_name = '%s.%s' % (prefix, name)
                    if len(rules) > 1:
                        route_name = '%s_%d' % (route_name, idx)

                    config.add_route(route_name, url)
                    config.add_view(function, route_name=route_name, **options)
            else:  # no decorators
                url = cls.build_url(name, name)
                route_name = '%s.%s' % (prefix, name)
                config.add_route(route_name, url)
                config.add_view(function, route_name=route_name)

    @classmethod
    def build_url(cls, name, url=''):
        if name == 'index':
            url = ''
        return '%s/%s' % (cls.route_base, url.lstrip('/'))

    @classmethod
    def make_proxy_method(cls, name):
        view = getattr(cls(), name)
        for decorator in cls.decorators:
            view = decorator(view)
        return view
