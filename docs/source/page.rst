Pages - Structuring your application
***************************************
With `borobudur.page.PageRoutingPolicy`, routing consists of mappings from url pattern to ``Page``. When a url pattern matches,
borobudur will create an instance of the supplied Page. a ``Page`` can have a parent page, and that parent can also
have another parent, Borobudur will create a page hierarchy, and opening them from top to down

To use this routing policy, set `routing_policy` parameter in `AppConfigurator` constructor to an instance of `PageRoutingPolicy`

When a page is opened, it typically manages its models (e.g. by retrieving from ``Resources``) and renders views
based on its models. On a browser, retrieving models must be done asynchronously, and pages code can be ugly
really fast. Fortunately, Page API hides them  (and page's code can be flat) by its two overiddable methods:

* ``prepare``: all async invoking operation should be done here
* ``open``: invoked when all async operation finished.


Here is a sample page:


    .. pycco:: python

        from borobudur.view import View
        from borobudur.page import Page
        from borobudur.page.loaders import StorageLoader

        class InquiryView(View):
            pass

        #some simple `Page` to act as parent
        class DashboardPage(Page):

            def echo(self, text):
                print text

        class InquiryPage(Page):

            #specify that `DashboardPage` must be loaded before this page loads
            parent_page_type = DashboardPage

            #tells whether this page and its children should be rendered in client, or both in server and client,
            #defaults to `False`
            client_only = False

            #when routed in client, borobudur reuse previous pages that also exists in the current route.
            #A page can tell borobudur to reload it in the next route by overriding this `will_reload` method and returns
            #`True`
            def will_reload(self, request):
                #a request have `matchdict` and `params` attributes
                return self.created_matchdict["id"] != request.matchdict["id"]


            #A `prepare` method accepts `loaders` which is a async operation collecting object
            def prepare(self, loaders):
                #a page has access to parent page instance in `parent_page` attributes
                self.parent_page.echo("hello")

                #initialize models
                self.models["inquiry"] = Inquiry({"_id": self.request.matchdict["id"]})
                #tell loaders to add fetch async operation to inquiry
                loaders.add(StorageLoader(self.models["inquiry]))

            #This method will be invoked when previous `loaders` finish all its async operation
            def open(self):
                #add view to document with element selector, view type, and view's model
                self.add_view("#content", InquiryView, self.models["inquiry"])

                #set document title
                self.title = "Inquiry - %s" %self.models["inquiry"]["name"]

When a Page is opened, borobudur will set html document attributes based on these Page's attributes:

    title
        sets to ``<title>{title}</title>``
    keywords
        sets to ``<meta name="keywords" content="{keywords}" />``
    description
        sets to ``<meta name="description" content="{description}" />``

Loaders
=======
page's `prepare` method manipulates `borobudur.page.loaders.Loaders` object. this object has `append` method to add
new `Loader`. Borobudur provides two loader, `borobudur.page.loaders.StorageLoader` and `borobudur.page.loaders.ServiceLoader`

`StorageLoader` accept model or collection in its constructor, for example

    .. code-block:: python

        model = User.with_id(121)
        loaders.append(StorageLoader(model))

`ServiceLoader` accept model or collection, `service_id`, and `service_attribute` in its constructor, for example

    .. code-block:: python

        model = Session()
        loaders.append(ServiceLoader(model, "session", "get"))

You can also define a custom loader, a loader must have `load` method which accept `request` and `callbacks`.
`callbacks.success()` must be invoked when a loader finishes its load operation.



    .. code-block:: python

        class CustomLoader(object):
            def __init__(self, model):
                self.model = model

            def load(self, request, callbacks):
                def json_callback(json):
                    self.model["info"] = json
                    callbacks.success()

                ElQuery.getJSON("somejsonurl", json_callback)

