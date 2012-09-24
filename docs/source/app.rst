Your first Borobudur single page application
*********************
A borobudur application is a  `single page application <http://en.wikipedia.org/wiki/Single-page_application>`_ except that first
request will be routed and rendered in server. Then, your client code can routes and render subsequent urls with binding every `<a>` elements to `app.router.navigate()`

Borobudur is based on `pyramid <http://www.pylonsproject.org/>`_ , and this guide assumes you have created a trivial pyramid application,
if not, read `creating simple pyramid application <http://pyramid.readthedocs.org/en/latest/narr/firstapp.html>`_

It also assumes you have already installed a python environment and pyramid, if not head to `installing pyramid <http://pyramid.readthedocs.org/en/latest/narr/install.html>`_

Installing borobudur
====================================
    .. code-block:: text

        pip install borobudur


Simplest borobudur app
=====================================
The very simplest borobudur application requires 3 files, (yes, it sucks)

You can generate these file by these commands
    .. code-block:: text

        mkdir test
        cd test
        borobudur create_simples

__init__.py:
    .. code-block:: python

        from pyramid.config import Configurator
        from borobudur.config import AppConfigurator
        from borobudur.asset import AssetManager
        from prambanan.library import PythonModule
        from prambanan import get_template
        from wsgiref.simple_server import make_server
        import views

        if __name__ == '__main__':
            config = Configurator()
            config.include("borobudur")

            asset_manager = AssetManager(
                base_dir="roma",
                static_dir="static",
                result_dir="gen",
                prambanan_dir=".p",
                prambanan_cache_file=".prambanan.cache",
            )
            asset_manager.add_module(PythonModule("views.py", modname="views"))

            app_config = AppConfigurator(
                asset_manager = asset_manager,
                base_template=prambanan.get_template("zpt", ("roma", "templates/test/simple.pt")),
            )
            app_config.add_route("foo", views.foo)
            app_config.add_route("bar", views.bar)
            app_config.add_bootstrap_subscriber("views:client_main")

            config.add_borobudur("hello", app_config, root="/")

            wsgi_app = config.make_wsgi_app()
            server = make_server('0.0.0.0', 8080, wsgi_app)
            server.serve_forever()

views.py
    .. code-block:: python

        import borobudur
        import prambanan
        from pramjs.elquery import ElQuery

        __author__ = 'h'

        def client_main(app_name, app):
            def on_click(ev):
                url = ElQuery(ev.currentTarget).attr("href")
                app.router.navigate(url)
                return False
            ElQuery("a", prambanan.document).click(on_click)

        def foo(request, callbacks):
            text = "foo rendered on %s" %("server" if borobudur.is_server else "client")
            ElQuery("#view", request.document).html(text)
            callbacks.success()

        def bar(request, callbacks):
            text = "bar rendered on %s" %("server" if borobudur.is_server else "client")
            ElQuery("#view", request.document).html(text)
            callbacks.success()

template.pt
    .. code-block:: html

        <!DOCTYPE html>
        <html>
            <head>
                <title>Hello borobudur</title>
            </head>

            <body>
                <div>
                    <a href="foo">foo</a>
                    <a href="bar">bar</a>
                </div>
                <div id="view"></div>
            </body>
        </html>

Then you can run those file by:

    .. code-block:: text

        python __init__.py


Asset Manager
-----------------------------------
    .. code-block:: python

            asset_manager = AssetManager(
                base_dir="roma",
                static_dir="static",
                result_dir="gen",
                prambanan_dir=".p",
                prambanan_cache_file=".prambanan.cache",
            )

Asset manager, as the name implies, manage js and css assets, it is responsible for compiling python to javascript, combining javascript files,
minifying css, etc

And with the following line, you register file views.py to be compilable to javascript with views as its modname

    .. code-block:: python

        asset_manager.add_module(PythonModule("views.py", modname="views"))


Single Page App Configurator
-----------------------------------

Before creating a single page application, create its configurator, with asset manager as parameter. Base template is used for template for any
routes in the single page application


    .. code-block:: python

            app_config = AppConfigurator(
                asset_manager = asset_manager,
                base_template=prambanan.get_template("zpt", ("roma", "templates/test/simple.pt")),
            )

You can add your route and its handler with

    .. code-block:: python

            app_config.add_route("foo", views.foo)
            app_config.add_route("bar", views.bar)

Subscribe to client bootstrap
-----------------------------------
You can listen to client app bootstrap by adding a bootstrap subscriber. This line

    .. code-block:: python

            app_config.add_bootstrap_subscriber("views:client_main")

adds this subscriber

    .. code-block:: python

        def client_main(app_name, app):
            def on_click(ev):
                url = ElQuery(ev.currentTarget).attr("href")
                app.router.navigate(url)
                return False
            ElQuery("a", prambanan.document).click(on_click)

which binds every anchor click to be routed by client

What routes handler do
-----------------------------------
This route handler create a text based on whether app is executed on client or server, then put it as #view content

    .. code-block:: python

        def foo(request, callbacks):
            text = "foo rendered on %s" %("server" if borobudur.is_server else "client")
            ElQuery("#view", request.document).html(text)
            callbacks.success()

