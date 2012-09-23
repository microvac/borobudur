from __future__ import with_statement
from pyramid.renderers import render_to_response
from borobudur.interfaces import IBootstrapSubscriber, IAppConfigurator
from pyramid_debugtoolbar.panels import DebugPanel

_ = lambda x: x

class AssetDebugPanel(DebugPanel):
    """
    Panel that looks at the performance of a request.

    It will display the time a request took and, optionally, the
    cProfile output.
    """
    name = 'Asset'
    has_content = True

    def __init__(self, request):
        self.request = request

    def wrap_handler(self, handler):
        handler = self._wrap_live_edit_handler(handler)
        return handler

    def _wrap_live_edit_handler(self, handler):
        return handler

    def title(self):
        return _('Assets')

    def nav_title(self):
        return _('Assets')

    def url(self):
        return ''

    def content(self):
        vars = {}
        return self.render(
            'borobudur.debugtoolbar.server:asset.dbtmako',
            vars, request=self.request)

def asset_list_view(request):
    page_type_id = request.matchdict["handler_qname"]

    app_name = request.matchdict["app_name"]
    app_config = request.registry.getUtility(IAppConfigurator, name=app_name)
    subscribers = app_config.get_bootstrap_subscribers(request)
    calculate = app_config.asset_calculator

    packs = list(calculate(app_name, subscribers, page_type_id))
    styles = ["bootstrap"]

    results = {
        "css": {},
        "js": {},
        }

    asset_manager = app_config.asset_manager
    for type, name, bundle in asset_manager.get_all_bundles(packs, styles):
        results[type][name] = [url for url in bundle.urls(asset_manager.env)]

    return render_to_response("json", results)


def asset_changed_view(request):
    page_type_id = request.matchdict["handler_qname"]

    app_name = request.matchdict["app_name"]
    app_config = request.registry.getUtility(IAppConfigurator, name=app_name)
    subscribers = app_config.get_bootstrap_subscribers(request)
    calculate = app_config.asset_calculator

    import time

    packs = list(calculate(app_name, subscribers, page_type_id))
    styles = ["bootstrap"]

    results = {"js": [], "css": []}

    asset_manager = app_config.asset_manager

    found = False
    i = 0
    while not found and i < 1000:
        for type, name, bundle in asset_manager.get_all_bundles(packs, styles):
            if asset_manager.env.updater.needs_rebuild(bundle, asset_manager.env):
                results[type].append(name)
                found = True
            i += 0
        if not found:
            time.sleep(1)

    return render_to_response("json", results)



