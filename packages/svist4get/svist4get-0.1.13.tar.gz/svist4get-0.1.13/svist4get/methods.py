import configs


import io
from wand.image import  Image, Color


import os
import sys
import shutil

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    tup =  tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    out = []
    for i in tup:
        out.append(i/255)
    return(out)


def pdf_page_to_png(parameters):
    resolution = parameters.config['png_dpi']
    filename = parameters.config['output_filename']
    page = Image(filename = filename, resolution = resolution)
    page.format = 'png'
    page.background_color = Color('white')
    page.alpha_channel = 'remove'


    image_filename = os.path.splitext((filename))[0] + '.png'
    #image_filename = filename + '.png'
    #image_filename = '{}-{}.png'.format(image_filename, page)
    #image_filename = os.path.join('./', image_filename)


    page.save(filename = image_filename)
    print('Image successfully saved to', image_filename)

def path_manager():
    users_path = os.getcwd()
    inside_path = os.path.dirname(__file__, '')

    paths = dict(users_path = users_path, inside_path = inside_path)

    return(paths)


