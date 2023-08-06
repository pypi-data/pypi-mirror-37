

import json

from django.conf import settings
from django.http import HttpResponse
from django.views.generic.base import View
from py_mini_racer.py_mini_racer import MiniRacerBaseException

from zmei.json import ZmeiReactJsonEncoder
from zmei.react import ZmeiReactServer


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


class ZmeiReactViewMixin(ZmeiDataViewMixin):

    react_server = None
    react_components = None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if 'application/json' in self.request.META['HTTP_ACCEPT']:
            return HttpResponse(context['react_state'], content_type='application/json')

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if not isinstance(self.react_server, ZmeiReactServer):
            raise ImproperlyConfigured('ZmeiReactViewMixin requires react_server property')

        if not isinstance(self.react_components, list):
            raise ImproperlyConfigured('ZmeiReactViewMixin requires react_component property')

        data['react_state'] = ZmeiReactJsonEncoder(view=self).encode(self._get_data())

        if settings.DEBUG:
            self.react_server.autreload()

        for cmp in self.react_components:
            try:
                data[f'react_page_{cmp}'] = self.react_server.evaljs(f"R.renderServer(R.{cmp}Reducer, R.{cmp}, {data['react_state']});")
            except MiniRacerBaseException as e:
                data[f'react_page_{cmp}'] = f'<script>var err = {json.dumps({"msg": str(e)})}; ' \
                                            f'document.body.innerHTML = ' \
                                            "'<h2>Error rendering React component. See console for details.</h2>' + " \
                                            f'"<pre>" + err.msg + "</pre>" + document.body.innerHTML;</script>'

        return data
