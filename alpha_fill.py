#!/usr/bin/env python

# Tutorial available at: https://www.youtube.com/watch?v=nmb-0KcgXzI
# Feedback welcome: jacksonbates@hotmail.com

from gimpfu import *

def layer_to_image(layer):
    buffer = pdb.gimp_edit_named_copy(layer, "LAYER")
    new_image = pdb.gimp_edit_named_paste_as_new_image(buffer)
    return new_image

def alpha_fill(image, drawable, color):
    # function code goes here...
    layer = image.active_layer
    decomposed = pdb.plug_in_decompose(image, layer, "RGBA", 1)[0]

    foreground = pdb.gimp_context_get_foreground()

    pdb.gimp_context_set_foreground(gimpcolor.RGB(color.r,color.r,color.r))
    pdb.gimp_drawable_fill(decomposed.layers[0], 0)

    pdb.gimp_context_set_foreground(gimpcolor.RGB(color.g,color.g,color.g))
    pdb.gimp_drawable_fill(decomposed.layers[1], 0)

    pdb.gimp_context_set_foreground(gimpcolor.RGB(color.b,color.b,color.b))
    pdb.gimp_drawable_fill(decomposed.layers[2], 0)

    pdb.gimp_context_set_foreground(foreground)

    red = layer_to_image(decomposed.layers[0])
    green = layer_to_image(decomposed.layers[1])
    blue = layer_to_image(decomposed.layers[2])
    alpha = layer_to_image(decomposed.layers[3])

    composed = pdb.plug_in_compose(red, drawable, green, blue, alpha, "RGBA")
   
    pdb.gimp_drawable_edit_clear(layer)

    pdb.gimp_edit_copy(composed.layers[0])
    FloatingLayer = pdb.gimp_edit_paste(layer, TRUE)
    pdb.gimp_floating_sel_anchor(FloatingLayer)


register(
    "python-fu-alpha-fill",
    "Alpha fill",
    "Fills an entire image with a specific color considering alpha",
    "extreampolice", "extreampolice", "2025",
    "Alpha fill",
    "RGBA", # type of image it works on (*, RGB, RGB*, RGBA, GRAY etc...)
    [
        # basic parameters are: (UI_ELEMENT, "variable", "label", Default)
        (PF_IMAGE, "image", "takes current image", None),
        (PF_DRAWABLE, "drawable", "Input layer", None),
        (PF_COLOR, "color", "colors", (0,0,0))
        # PF_SLIDER, SPINNER have an extra tuple (min, max, step)
        # PF_RADIO has an extra tuples within a tuple:
        # eg. (("radio_label", "radio_value), ...) for as many radio buttons
        # PF_OPTION has an extra tuple containing options in drop-down list
        # eg. ("opt1", "opt2", ...) for as many options
        # see ui_examples_1.py and ui_examples_2.py for live examples
    ],
    [],
    alpha_fill, menu="<Image>")  # second item is menu location

main()