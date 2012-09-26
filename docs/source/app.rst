Your first Borobudur single page application
*********************
A borobudur application is a  `single page application <http://en.wikipedia.org/wiki/Single-page_application>`_ with an exception
that the first request of any page will be routed and rendered in server. After the first request is routed and rendered,
the rest will be the same as single page application. Thus, the implication of this method is that the logic of application
exists in server and client.

Borobudur is based on `pyramid <http://www.pylonsproject.org/>`_ , and this guide assumes that:
    #. you have an understanding in creating a `basic pyramid application <http://pyramid.readthedocs.org/en/latest/narr/firstapp.html>`_.
    #. you have already installed a python environment and pyramid, if you haven't you can go to `installing pyramid <http://pyramid.readthedocs.org/en/latest/narr/install.html>`_

Installing borobudur
====================================
    .. code-block:: text

        pip install borobudur


Simplest borobudur app
=====================================
The very simplest borobudur application requires a minimum of 3 files, (yes, it sucks)

You can generate these files by these commands:
    .. code-block:: text

        mkdir test
        cd test
        borobudur create_simples

Then, you create these three files:

    .. pycco:: python

        # **__init_.py** file which is executed in server only
        #It create a pyramid wsgi app and add a borobudur ap to it
        from pyramid.config import Configurator
        from borobudur.config import AppConfigurator
        from borobudur.asset import AssetManager
        from prambanan.library import PythonModule
        from prambanan import get_template
        from wsgiref.simple_server import make_server
        import views

        if __name__ == '__main__':
            #create pyramid configurator
            config = Configurator()

            #tell config to execute 'borobudur.config' module
            config.include("borobudur.config")

            #Asset manager, as the name implies, manage js and css assets, it is responsible for compiling python to javascript,
            #combining javascript files,minifying css, etc
            asset_manager = AssetManager(
                base_dir="roma",
                static_dir="static",
                result_dir="gen",
                prambanan_dir=".p",
                prambanan_cache_file=".prambanan.cache",
            )

            #register file views.py to be compilable to javascript with views as its modname
            asset_manager.add_module(PythonModule("views.py", modname="views"))

            #Before creating a single page application, create its configurator, with asset manager as parameter.
            #Base template is used for template for any routes in the single page application
            app_config = AppConfigurator(
                asset_manager = asset_manager,
                base_template=prambanan.get_template("zpt", ("roma", "templates/test/simple.pt")),
            )

            #Add route handlers in views module with the respective url patterns
            app_config.add_route("foo", views.foo)
            app_config.add_route("bar", views.bar)


            #Register 'views:client_main' function to be executed at client bootstrap.
            app_config.add_bootstrap_subscriber("views:client_main")

            #add the single page application to pyramid config
            config.add_borobudur("hello", app_config, root="/")

            #serve the wsgi application
            wsgi_app = config.make_wsgi_app()
            server = make_server('0.0.0.0', 8080, wsgi_app)
            server.serve_forever()

    .. pycco:: python

        #**views.py** which is executed in client and server.
        #it defines route handlers and a client bootstrap subscriber
        import borobudur
        import prambanan
        from pramjs.elquery import ElQuery

        #a callback to be executed in client bootstrap
        def client_main(app_name, app):
            def on_click(ev):
                #get `<a>` element href
                url = ElQuery(ev.currentTarget).attr("href")

                #tells client `app.router` to route and render the url
                app.router.navigate(url)

                #prevent default and stop propagation of click event
                return False

            #binds every a element in document with `on_click`,
            #because it is executed in client, it has access to global `prambanan.document`
            ElQuery("a", prambanan.document).click(on_click)

        #handler to '/foo' route
        def foo(request, callbacks):

            #create some text depends on where this code is executed
            text = "foo rendered on %s" %("server" if borobudur.is_server else "client")

            #put that text to `#view` inner html.
            #Route handlers are executed in both client and server,
            #so use `request.document` instead of global `prambanan.document`
            ElQuery("#view", request.document).html(text)
            callbacks.success()

        #handler to '/bar' route
        def bar(request, callbacks):
            text = "bar rendered on %s" %("server" if borobudur.is_server else "client")
            ElQuery("#view", request.document).html(text)
            callbacks.success()

and **template.pt**
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

The next step is running those files with command:

    .. code-block:: text

        python __init__.py


