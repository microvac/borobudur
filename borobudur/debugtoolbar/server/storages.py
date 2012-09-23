from __future__ import with_statement


import threading

from pyramid_debugtoolbar.panels import DebugPanel
from borobudur.config import get_borobudur_app

_ = lambda x: x

class StoragesDebugPanel(DebugPanel):
    """
    Panel that looks at the performance of a request.

    It will display the time a request took and, optionally, the
    cProfile output.
    """
    name = 'Storages'
    has_content = True

    def __init__(self, request):
        self.request = request
        self.app = get_borobudur_app(request)

    def wrap_handler(self, handler):
        handler = self._wrap_live_edit_handler(handler)
        return handler

    def _wrap_live_edit_handler(self, handler):
        return handler

    def title(self):
        return _('Storages')

    def nav_title(self):
        return _('Storages')

    def url(self):
        return ''

    def content(self):
        vars = {"app": self.app}
        return self.render(
            'borobudur.debugtoolbar:storages.dbtmako',
            vars, request=self.request)

