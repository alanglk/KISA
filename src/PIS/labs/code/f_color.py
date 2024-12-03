# f_color.py

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as im

from matplotlib import colormaps
from matplotlib.colors import LinearSegmentedColormap

from sklearn.cluster import KMeans

from collections import Counter

def RGB_HEX(color):
     return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2])) 

def mapsColorsCYM():
    cm_cyans    = LinearSegmentedColormap.from_list('cyans', [(0,0,0), (0,1,1)])
    # colormaps.register(cm_cyans, force=True)
    cm_yellows  = LinearSegmentedColormap.from_list('yellows', [(0,0,0), (1,1,0)])
    # colormaps.register(cm_yellows, force=True)
    cm_magentas = LinearSegmentedColormap.from_list('magentas', [(0,0,0), (1,0,1)])
    # colormaps.register(cm_magentas, force=True)
    return cm_cyans, cm_yellows, cm_magentas

def RGBtoCMYK(rgb): 
    # https://imagej.net/tutorials/rgb-to-cmyk

    k = 1 - np.max(rgb, axis=2)
    kte = 255/(1 - k)
    
    with np.errstate(divide="ignore", invalid="ignore"):
        # Calculate C
        c = (1 - rgb[..., 0] - k) * kte
        c = c.astype(np.uint8)

        # Calculate M
        m = (1 - rgb[..., 1] - k) * kte
        m = m.astype(np.uint8)

        # Calculate Y
        y = (1 - rgb[..., 2] - k) * kte
        y = y.astype(np.uint8)
    
    cmyk = np.dstack((c, m, y, k))
    
    return cmyk

def CMYKtoRGB(cmyk):
    # https://www.101computing.net/cmyk-to-rgb-conversion-algorithm/

    aux = cmyk.astype(float)/100.0
    k = aux[:,:,3]
    
    r = (1 - cmyk[:, :, 0]) * (1 - k)
    g = (1 - cmyk[:, :, 1]) * (1 - k)
    b = (1 - cmyk[:, :, 2]) * (1 - k)
    
    rgb = (np.dstack((r, g, b))*255.0).astype(np.uint8)

    return rgb

def quantify_colors(im, n_colores):
    """Quantify the colors of imagen
      
    Args: 
        im: image
        n_colores: number of colors
    """
    (h,w,c) = im.shape
    im_r    = im.reshape(h*w, c)
    modelo  = KMeans(n_clusters = n_colores)
    etiquetas = modelo.fit_predict(im_r)
    counts    = Counter(etiquetas)
    counts    = dict(sorted(counts.items()))
    centros   = np.array(modelo.cluster_centers_)
    colores   = np.array([centros[i] for i in counts.keys()])*255.0
    colores_hex = np.array([RGB_HEX(colores[i]) for i in counts.keys()])
    paleta = np.uint8(colores)
    im_q = paleta[etiquetas.flatten()]
    im_q = im_q.reshape(im.shape)
    return counts, paleta, colores_hex, im_q