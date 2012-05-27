import prambanan

is_server = not prambanan.is_js

def add_borobudur_app(config, app):
    app.config = config

def includeme(config):
    config.add_directive('add_borobudur_app', add_borobudur_app)
