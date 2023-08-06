"""

conversions.py

@author: derricw

Conversion functions.

"""
from bisect import bisect
import random
import os

from PIL import Image, ImageOps, ImageDraw, ImageFont
import numpy as np
import cv2
import imageio

from asciisciit.misc import *
from asciisciit.lut import get_lut, relative_width

DEFAULT_ASPECT_CORRECTION_FACTOR = 6.0/11.0
RESOURCE_DIR = os.path.join(os.path.dirname(__file__),'res')


def image_to_ascii(img,
                   scalefactor=0.2,
                   invert=False,
                   equalize=True,
                   lut='simple',
                   aspect_correction_factor=None):
    """
    Generates and ascii string from an image of some kind.

    Parameters
    ----------
    img : str, ndarray, PIL.Image
        Image to convert
    scalefactor : float
        ASCII chars per pixel
    invert : bool
        Invert luminance?
    equalize : bool
        Equalize histogram?

    Returns
    -------
    str

    Examples
    --------

    >>> ascii_img = image_to_ascii("http://i.imgur.com/l2FU2J0.jpg", scalefactor=0.3)
    >>> print(ascii_img)

    """
    if type(img) == str:
        img = open_pil_img(img)
    elif type(img) == np.ndarray:
        img = numpy_to_pil(img)
    try:
        text = pil_to_ascii(img, scalefactor, invert, equalize, lut,
                            aspect_correction_factor)
    except:
        raise TypeError("That image type doesn't work.  Try PIL, Numpy, or file path...")
    return text


def pil_to_ascii(img,
                 scalefactor=0.2,
                 invert=False,
                 equalize=True,
                 lut='simple',
                 aspect_correction_factor=None
                 ):
    """
    Generates an ascii string from a PIL image.

    Parameters
    ----------
    img : PIL.Image
        PIL image to transform.
    scalefactor : float
        ASCII characters per pixel.
    invert : bool
        Invert luminance?
    equalize : bool
        equalize histogram (for best results do this).
    lut : str
        Name of the lookup table to use. Currently supports 'simple' and
        'binary'.

    Returns
    -------
    str

    Examples
    --------

    >>> from asciisciit.misc import open_pil_img
    >>> img = open_pil_img("http://i.imgur.com/l2FU2J0.jpg")
    >>> text_img = pil_to_ascii(img, scalefactor=0.3)
    >>> print(text_img)

    >>> from PIL import Image
    >>> img = Image.open("some_image.png")
    >>> text_img = pil_to_ascii(img)
    >>> print(text_img)

    """
    lookup = get_lut(lut)
    if aspect_correction_factor is None:
        aspect_correction_factor = get_aspect_correction_factor(lookup.exemplar)

    img = img.resize(
        (int(img.size[0]*scalefactor), 
         int(img.size[1]*scalefactor*aspect_correction_factor)),
        Image.BILINEAR)
    img = img.convert("L")  # convert to mono
    if equalize:
        img = ImageOps.equalize(img)

    if invert:
        img = ImageOps.invert(img)

    img = np.array(img, dtype=np.uint8)

    return u"\n" + u"".join(lookup.apply(img).flatten().tolist())


def ascii_to_pil(text, font_size=10, bg_color=(20, 20, 20),
                 fg_color=(255, 255, 255), font_path=None):
    """
    Renders Ascii text to an Image of the appropriate size, using text of the
        specified font size.

    Parameters
    ----------
    text : str
        Ascii text to render.
    font_size : int (10)
        Font size for rendered image.
    bg_color : tuple (20,20,20)
        (R,G,B) values for image background.
    fg_color : tuple (255,255,255)
        (R,G,B) values for text color. -1 gets value from image.
    font_path : str
        Use a custom font .ttf file.

    Returns
    -------
    PIL.Image

    Examples
    --------

    >>> ascii = AsciiImage("http://i.imgur.com/l2FU2J0.jpg", scalefactor=0.4)
    >>> pil = ascii_to_pil(ascii.data)
    >>> pil.show()

    """
    font = get_font(font_path, font_size)
    if relative_width(text[1]) == 2:
        font_width, font_height = font.getsize(u"\u3000")
    else:
        font_width, font_height = font.getsize(u" ")

    img_height, img_width = get_ascii_image_size(text)

    y_padding = 1

    out_img = np.zeros(((font_height+y_padding)*img_height, 
                         font_width*img_width,
                         3),
                       dtype=np.uint8)
    out_img[:, :, 0] += bg_color[0]
    out_img[:, :, 1] += bg_color[1]
    out_img[:, :, 2] += bg_color[2]

    img = Image.fromarray(out_img)
    draw = ImageDraw.Draw(img)

    for index, line in enumerate(text.split("\n")):
        y = (font_height+y_padding)*index
        draw.text((0, y), line, fg_color, font=font)
    return img


def ascii_seq_to_gif(seq, output_path, fps=15.0, font_size=10,
                     font_path=None):
    """ Creates a gif from a sequence of ascii images.

        Parameters
        ----------
        output_path : str
            Path for gif output.
        fps : float
            FPS for gif playback.
        font_size : int
            Font size for ascii.
    """
    images = []

    status = StatusBar(len(seq), text="Generating frames: ",)

    for index, ascii_img in enumerate(seq):
        if type(ascii_img) == str:
            #raw text
            text = ascii_img
        else:
            #AsciiImage instance
            text = ascii_img.data
        images.append(
            ascii_to_pil(text,
                         font_size=font_size,
                         font_path=font_path
                        )
                    )
        status.update(index)

    status.complete()

    duration = 1.0/fps

    images_np = [np.array(img) for img in images]
    imageio.mimsave(output_path, images_np, duration=duration)


def numpy_to_ascii(img,
                   scalefactor=0.2,
                   invert=False,
                   equalize=True,
                   lut="simple",
                   aspect_correction_factor=None):
    """
    Generates an ascii string from a numpy image.

    Parameters
    ----------
    img : ndarray
        PIL image to transform.
    scalefactor : float
        ASCII characters per pixel.
    invert : bool
        Invert luminance?
    equalize : bool
        equalize histogram (for best results do this).
    lut : str
        Name of the lookup table to use. Currently supports 'simple' and
        'binary'.

    Returns
    -------
    str
    """
    lookup = get_lut(lut)
    if aspect_correction_factor is None:
        aspect_correction_factor = get_aspect_correction_factor(lookup.exemplar)
    h, w = img.shape

    img = cv2.resize(
        img,
        (
            int(w*scalefactor),
            int(h*scalefactor*aspect_correction_factor)
        )
    )

    if img.ndim == 3: # weak check for RGB
        # works in opencv 3.4.3 but who knows, they keep moving/renaming stuff
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    if equalize:
        img=cv2.equalizeHist(img)

    if invert:
        img = 255-img

    return u"\n" + u"".join(lookup.apply(img).flatten().tolist())


def image_to_numpy(path):
    """
    Image file to numpy matrix.
    """
    img = open_pil_img(path)
    return np.array(img, dtype=np.uint8)


def numpy_to_pil(nparray):
    """
    Numpy matrix to PIL Image.
    """
    return Image.fromarray(nparray)


def get_font(font_path=None, font_size=10):
    if not font_path:
        font_path = os.path.join(RESOURCE_DIR, "Cousine-Regular.ttf")

    return ImageFont.truetype(font_path, font_size)


def get_aspect_correction_factor(exemplar, font_path=None, font_size=10):
    if font_path is None:
        factor = relative_width(exemplar)*DEFAULT_ASPECT_CORRECTION_FACTOR
    else:
        font = get_font(font_path, font_size)
        width, height = font.getsize(exemplar)
        factor = float(width) / height

    return factor


def gif_to_numpy(gif_path):
    """
    Converts a GIF into a numpy movie.
    """
    gif = open_pil_img(gif_path)
    if hasattr(gif, 'info'):
        frame_duration = gif.info.get('duration', None)
    else:
        frame_duration = None
    length = get_length_of_gif(gif)

    size = gif.size
    
    status = StatusBar(length, "Reading frames: ")

    frames = []
    frame_count = 0
    while gif:
        new_img = Image.new("RGBA",size)
        new_img.paste(gif)
        frames.append(new_img)
        frame_count += 1
        try:
            gif.seek(frame_count)
        except EOFError:
            break
        status.update(frame_count)

    status.complete()

    assert(length==len(frames))

    final_frame_count = len(frames)
    frame1 = np.array(frames[0])
    shape = frame1.shape
    matrix = np.zeros((final_frame_count,shape[0],shape[1],shape[2]), dtype=np.uint8)
    for i, frame in enumerate(frames):
        img = np.asarray(frame)
        matrix[i] = img
    return matrix, frame_duration


def figure_to_numpy(mpl_figure):
    """
    Converts a matplotlib figure to numpy matrix.
    """
    mpl_figure.tight_layout(pad=0.1)
    mpl_figure.canvas.draw()
    data = np.fromstring(mpl_figure.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(mpl_figure.canvas.get_width_height()[::-1]+ (3,))
    return data


def figure_to_ascii(mpl_figure):
    """
    Converts a matplotlib figure to ascii image.
    """
    npy_fig = figure_to_numpy(mpl_figure)
    return image_to_ascii(npy_fig, scalefactor=0.15, invert=False, equalize=False)


if __name__ == '__main__':
    pass
