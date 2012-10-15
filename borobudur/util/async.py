from prambanan import JS

def serial_save(resourcer, models, success=None, error=None):
    i = 0
    def next():
        global i
        if i == len(models):
            if success is not None:
                success()
        else:
            model = models[i]
            i += 1
            resourcer.save(model, success=next)
    next()