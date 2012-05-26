import borobudur

app = borobudur.App(
    base_template="template/base.pt",
    packages = {
        "main": {
            "python" : ["app.py", "entities/", "views/", "pages/"],
            "templates": ["templates/"]
        }
    }
)
