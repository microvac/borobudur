from borobudur.debugtoolbar.asset import AssetDebugPanel

def includeme(config):
    config.add_static_view('_debug_toolbar_borobudur/static/', "borobudur.debugtoolbar:static/")
    config.registry.settings['debugtoolbar.panels'].append(AssetDebugPanel)
    if not 'mako.directories' in config.registry.settings:
        config.registry.settings['mako.directories'] = []