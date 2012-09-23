from borobudur.debugtoolbar.server.api_invocation import APIInvocationDebugPanel
from borobudur.debugtoolbar.server.asset import AssetDebugPanel, asset_changed_view, asset_list_view

def includeme(config):
    config.add_static_view('_debug_toolbar_borobudur/static/', "borobudur.debugtoolbar:static/")
    config.registry.settings['debugtoolbar.panels'].extend([AssetDebugPanel, APIInvocationDebugPanel])#, StoragesDebugPanel])
    if not 'mako.directories' in config.registry.settings:
        config.registry.settings['mako.directories'] = []

    config.add_global_bootstrap_subscriber("borobudur.debugtoolbar.client.api_invocation:main")
    config.add_global_bootstrap_subscriber("borobudur.debugtoolbar.client.asset:main")

    al_route_name = "debug_toolbar.borobudur.asset.list"
    config.add_route(al_route_name, "_debug_toolbar_borobudur/assets/list/{app_name}/{handler_qname}")
    config.add_view(asset_list_view, route_name=al_route_name)

    ac_route_name = "debug_toolbar.borobudur.asset.changed"
    config.add_route(ac_route_name, "_debug_toolbar_borobudur/assets/changed/{app_name}/{handler_qname}")
    config.add_view(asset_changed_view, route_name=ac_route_name)
