# f_halftone.py

import sys
import os

import random

import numpy as np

from skimage.color import rgb2gray, rgba2rgb
from skimage.filters import threshold_otsu

from tqdm import tqdm

# Ajuste de los niveles de grises
def adjust_gray(im, new_min, new_max):
    im_min = np.min(im)
    im_max = np.max(im)
    h, w  = im.shape
    adj = (im - im_min)*((new_max - new_min)/(im_max - im_min)) + new_min
    return adj.astype(np.uint8)

# Convertir la imagen a escala de grises
def convert_grayscale(im):
    if (len(im.shape)==3):
        # luminancia
        im_g = 0.299*im[:, :, 0] + 0.587*im[:, :, 1] + 0.114*im[:, :, 2]
        return im_g
    else:
        return im

# Mascaras halftone
def gen_halftone_masks():
    m = np.zeros((3, 3, 10))

    m[:, :, 1] = m[:, :, 0]
    m[0, 1, 1] = 1

    m[:, :, 2] = m[:, :, 1]
    m[2, 2, 2] = 1

    m[:, :, 3] = m[:, :, 2]
    m[0, 0, 3] = 1

    m[:, :, 4] = m[:, :, 3]
    m[2, 0, 4] = 1

    m[:, :, 5] = m[:, :, 4]
    m[0, 2, 5] = 1

    m[:, :, 6] = m[:, :, 5]
    m[1, 2, 6] = 1

    m[:, :, 7] = m[:, :, 6]
    m[2, 1, 7] = 1

    m[:, :, 8] = m[:, :, 7]
    m[1, 0, 8] = 1

    m[:, :, 9] = m[:, :, 8]
    m[1, 1, 9] = 1

    return m

# Suavizado de tonos (halftone) en el dominio espacial
def halftone(im):
    m    = gen_halftone_masks()
    im_g = convert_grayscale(im)
    im_g = adjust_gray(im_g, 0, 9)
    h, w = im_g.shape
    
    im_h = np.zeros((3*h, 3*w))
    for j in tqdm(range(h), desc = "halftone"):
        for i in range(w):
            ii = im_g[j, i]
            im_h[3*j:3+3*j, 3*i:3+3*i] = m[:, :, ii]
    im_h = 255*im_h
    return im_h