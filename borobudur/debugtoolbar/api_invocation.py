from __future__ import with_statement


import threading

from pyramid_debugtoolbar.panels import DebugPanel

_ = lambda x: x

class APIInvocationDebugPanel(DebugPanel):
    """
    Panel that looks at the performance of a request.

    It will display the time a request took and, optionally, the
    cProfile output.
    """
    name = 'APIInvocation'
    has_content = True

    def __init__(self, request):
        self.request = request

    def wrap_handler(self, handler):
        handler = self._wrap_live_edit_handler(handler)
        return handler

    def _wrap_live_edit_handler(self, handler):
        return handler

    def title(self):
        return _('API Invocations')

    def nav_title(self):
        return _('API Invocations')

    def nav_subtitle(self):
        return "-"

    def url(self):
        return ''

    def content(self):
        vars = {}
        return self.render(
            'borobudur.debugtoolbar:api_invocation.dbtmako',
            vars, request=self.request)

