from borobudur.debugtoolbar.api_invocation import APIInvocationDebugPanel
from borobudur.debugtoolbar.asset import AssetDebugPanel
from borobudur.debugtoolbar.storages import StoragesDebugPanel

def includeme(config):
    config.add_static_view('_debug_toolbar_borobudur/static/', "borobudur.debugtoolbar:static/")
    config.registry.settings['debugtoolbar.panels'].extend([AssetDebugPanel, APIInvocationDebugPanel, StoragesDebugPanel])
    if not 'mako.directories' in config.registry.settings:
        config.registry.settings['mako.directories'] = []