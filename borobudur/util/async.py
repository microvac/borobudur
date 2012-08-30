from prambanan import JS

def serial(method, app, models, success=None, error=None):
    i = 0
    def next():
        global i
        if i == len(models):
            if success is not None:
                success()
        else:
            model = models[i]
            i += 1
            JS("model[method]")(app, success=next)
    next()