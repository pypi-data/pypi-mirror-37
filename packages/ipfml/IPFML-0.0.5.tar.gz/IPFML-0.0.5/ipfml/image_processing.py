from PIL import Image

import numpy as np

def fig2data(fig):
    """
    @brief Convert a Matplotlib figure to a 3D numpy array with RGB channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGB values
    """
    # draw the renderer
    fig.canvas.draw()
 
    # Get the RGBA buffer from the figure
    w,h = fig.canvas.get_width_height()
    buf = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8)
    buf.shape = (w, h, 3)
 
    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll(buf, 3, axis=2)
    return buf
    
def fig2img(fig):
    """
    @brief Convert a Matplotlib figure to a PIL Image in RGB format and return it
    @param fig a matplotlib figure
    @return a Python Imaging Library (PIL) image : default size (480,640,3)
    """
    # put the figure pixmap into a numpy array
    buf = fig2data(fig)
    w, h, d = buf.shape
    return Image.frombytes("RGB", (w, h), buf.tostring())