from prambanan import JS
import borobudur

def modal(el, options):
    JS("$(el).modal(options)")

def modal_gallery(el, options):
    JS("modal_gallery_show(el, options)")

