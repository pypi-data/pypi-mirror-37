

import json

from django.conf import settings
from django.http import HttpResponse
from django.views.generic.base import View



class _Data(object):
    def __init__(self, data=None):
        self.__dict__.update(data or {})

    def __add__(self, data):
        return _Data({**self.__dict__, **data})


class ZmeiDataViewMixin(View):
    _data = None

    def get_data(self, url, request, inherited):
        return {}

    def _get_data(self):
        if not self._data:
            self._data = self.get_data(
                url=type('url', (object,), self.kwargs),
                request=self.request,
                inherited=False
            )

        return self._data

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**self.kwargs)

        return {**context_data, **self._get_data()}


class ImproperlyConfigured(Exception):
    pass

