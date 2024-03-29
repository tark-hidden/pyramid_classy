# encoding: utf-8
"""
    Pyramid-Classy is an extension that adds class-based views to
    Pyramid more simple.
"""

from pyramid.compat import PY3
import inspect
import logging


def route(rule, **options):
    def decorator(f):
        if not hasattr(f, 'rules'):
            f.rules = []
        f.rules.append((rule, options))
        return f
    return decorator


def get_members(base, current):
    base_members = dir(base)
    predicate = PY3 and inspect.isfunction or inspect.ismethod
    all_members = inspect.getmembers(current, predicate=predicate)
    return [member for member in all_members
            if not member[0] in base_members and not member[0].startswith('_')]


class ClassyView(object):
    route_base = None
    debug = False
    __view_defaults__ = {}

    def __init__(self, request, context=None):
        self.request = request
        self.context = context

    @classmethod
    def register(cls, config, route_base=None, debug=False):
        n = cls.__name__
        log = logging.getLogger(config.registry.package_name)
        prefix = (n[:-4] if len(n) > 4 and n.endswith('View') else n).lower()

        if not route_base and not cls.route_base:
            cls.route_base = '/' if prefix == 'index' else '/%s/' % prefix
        elif route_base and route_base != '/':
            route_base_s = route_base.strip('/')
            cls.route_base = '/%s/' % route_base_s
            if prefix != route_base_s:
                prefix = '%s.%s' % (prefix, route_base_s)

        if debug:
            cls.debug = debug

        routes = []
        for name, _ in get_members(ClassyView, cls):
            view_defaults = cls.__view_defaults__.copy()
            if hasattr(getattr(cls, name), 'rules'):
                rules = getattr(cls, name).rules
                for idx, rule in enumerate(rules):
                    url, options = rule
                    url = cls.build_url(url)
                    route_name = options.pop('route_name', None)
                    view_defaults.update(options or {})
                    options = view_defaults

                    if not route_name:
                        route_name = '%s.%s' % (prefix, name)
                    if len(rules) > 1:
                        route_name = '%s_%d' % (route_name, idx)
                    routes.append((url, name, route_name, options))
            else:  # no decorators
                url = cls.build_url(name)
                route_name = '%s.%s' % (prefix, name)
                options = view_defaults
                routes.append((url, name, route_name, options))

        for rule in routes:
            url, name, route_name, options = rule
            config.add_route(route_name, url)
            config.add_view(cls, attr=name, route_name=route_name, **options)
            if cls.debug:
                log.debug("%s => '%s'" % (url, route_name))

    @classmethod
    def build_url(cls, url=''):
        return '%s%s' % (cls.route_base, url.lstrip('/'))
