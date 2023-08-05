#!/usr/bin/env python3

from PIL import Image, GifImagePlugin
import numpy
import sys
import click

def ansi_color_code(r, g, b):
    if r == g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return round(((r - 8) / 247) * 24) + 232
    return 16 \
        + (36 * round(r / 255 * 5)) \
        + (6 * round(g / 255 * 5)) \
        + round(b / 255 * 5)

def get_color(r, g, b):
    return "\x1b[48;5;{}m \x1b[0m".format(int(ansi_color_code(r,g,b)))

def print_image(image, width=69, aspect_ratio=0.5, show_title=False):
    img = Image.open(image)
    
    if hasattr(img, 'is_animated') and img.is_animated:
        img = img.convert('RGBA')

    w = width
    h = int((img.height / img.width) * w * aspect_ratio)

    img = img.resize((w,h), Image.ANTIALIAS)
    img_arr = numpy.asarray(img)
    h,w,_ = img_arr.shape

    if show_title:
        print('\n' + image)
    for x in range(h):
        for y in range(w):
            pix = img_arr[x][y]
            print(get_color(pix[0], pix[1], pix[2]), sep='', end='')
        print()

@click.command()
@click.argument('images', nargs=-1, required=True, type=str)
@click.option('-w', '--width', default=79, show_default=True)
@click.option('-a', '--aspect-ratio', default=0.5, show_default=True)
def main(images, width, aspect_ratio):
    if len(images) == 1:
        print_image(
            image=images[0],
            width=width,
            aspect_ratio=aspect_ratio,
            show_title=False
            )
        return

    errors = 0
    for image in images:
        try:
            print_image(
                image=image,
                width=width,
                aspect_ratio=aspect_ratio,
                show_title=True
                )
        except FileNotFoundError:
            print('Image not found: ' + image)
            errors += 1
        except Exception as e:
            print(str(e))
            errors += 1
    return errors

if __name__ == '__main__':
    main()

