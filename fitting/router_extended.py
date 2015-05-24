"""
Forked from django rest framework, we require much simpler and straight forward routes url handling
"""

from __future__ import unicode_literals
from collections import defaultdict
from django.views.generic import View

from rest_framework.routers import SimpleRouter as DRFSimpleRouter
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns


class ViewDispatcher(View):
    def __init__(self, *args, **kwargs):
        super(ViewDispatcher, self).__init__(*args, **kwargs)
        self.mapping = {}

    def dispatch(self, request, *args, **kwargs):
        method = request.method.lower()
        if method in self.mapping:
            return self.mapping[method](request, *args, **kwargs)
        else:
            return self.http_method_not_allowed(request, *args, **kwargs)

    def register(self, method, view):
        if method in self.mapping:
            raise RuntimeError("The method {} already registered".format(method))

        self.mapping[method] = view

    def convert_to_view(self):
        def view(request, *args, **kwargs):
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return self.dispatch(request, *args, **kwargs)

        return view


class SimpleRouter(DRFSimpleRouter):
    def __init__(self, *args, **kwargs):
        super(SimpleRouter, self).__init__(*args, **kwargs)

        self.dispatchers = defaultdict(ViewDispatcher)

    def get_urls(self):
        """
        Use the registered viewsets to generate a list of URL patterns.
        """
        ret = []

        for prefix, viewset, basename in self.registry:
            lookup = self.get_lookup_regex(viewset)
            routes = self.get_routes(viewset)

            for route in routes:
                mapping = self.get_method_map(viewset, route.mapping)
                if not mapping:
                    continue

                initkwargs = route.initkwargs
                # Build the url pattern
                if 'url' in initkwargs:
                    route_url = initkwargs.pop('url')
                    methods = [method for method, list in route.mapping.items()]
                    regex = route_url.format(
                        prefix=prefix
                    )
                    view = viewset.as_view(mapping, **route.initkwargs)
                    for method in methods:
                        print method + ' ' + regex
                        self.dispatchers[regex].register(method, view)
                else:
                    regex = route.url.format(
                        prefix=prefix,
                        lookup=lookup,
                        trailing_slash=self.trailing_slash
                    )
                    view = viewset.as_view(mapping, **initkwargs)
                    name = route.name.format(basename=basename)
                    ret.append(url(regex, view, name=name))

        for regex, dispatcher in self.dispatchers.items():
            ret.append(url(regex, dispatcher.convert_to_view()))

        return ret


class DefaultRouter(SimpleRouter):
    include_format_suffixes = True

    def get_urls(self):
        """
        Generate the list of URL patterns, including a default root view
        for the API, and appending `.json` style format suffixes.
        """
        urls = super(DefaultRouter, self).get_urls()
        if self.include_format_suffixes:
            urls = format_suffix_patterns(urls)

        return urls
