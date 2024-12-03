# f_get_random.py
import sys
import os

import random
from random import randrange

import numpy as np

##

def get_random_number(rango):
    if isinstance(rango, int):
        return randrange(start=0, stop=rango+1)
    else:
        return randrange(start=rango[0], stop=rango[1]+1)
    
def getN_random_number(rango, k):
    if isinstance(rango, int):
        conjunto = list(range(0, rango+1))
    else:
        conjunto = list(range(rango[0], rango[1]+1))
    return random.sample(conjunto, k)
    
def get_random_elements_of_list(lista, n):
    return random.sample(lista, n)

def get_images_path(folder_path):
    try:
        files = os.listdir(folder_path)
        # Filter the list to get only image files 
        images = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        if not images:
            print("No images found in the specified folder.")
            return None

        return images
    except Exception as e:
        print(f"An error occurred while selecting image randomly: {e}")
        return None

def get_random_image_path(folder_path):
    try:
        files = os.listdir(folder_path)
        # Filter the list to get only image files 
        images = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        if not images:
            print("No images found in the specified folder.")
            return None

        # Choose a random image file
        random_image = random.choice(images)
        random_image_path = os.path.join(folder_path, random_image)
        print(f"Here the random image path from the folder:")
        return random_image_path
    except Exception as e:
        print(f"An error occurred while selecting image randomly: {e}")
        return None

##

def get_audios_path(folder_path):
    try:
        files = os.listdir(folder_path)
        # Filter the list to get only audio files 
        audios = [file for file in files if file.lower().endswith(('.mp3', '.wav'))]
        print(audios)

        if not audios:
            print("No audios found in the specified folder.")
            return None

        return audios
    except Exception as e:
        print(f"An error occurred while selecting audio randomly: {e}")
        return None

def get_random_audio_path(folder_path):
    try:
        audios = get_audios_path(folder_path)

        if audios is None:
            return None
        else:
            # Choose a random audio file
            random_audio = random.choice(audios)
            random_audio_path = os.path.join(folder_path, random_audio)
            print(f"Here the random audio path from the folder:")
            return random_audio_path

    except Exception as e:
        print(f"An error occurred while selecting audio randomly: {e}")
        return None
    
## add noise

def add_noise(x, factor=2.5):
    x_noise = x + factor*np.random.randn(len(x))
    return x_noise

def add_noise_white(x, mu=0, sigma=2):
    x_noise = x + np.random.normal(mu, sigma, len(x))
    return x_noise

def add_noise_im(im, factor=200):
    im_noise = im + factor*np.random.randn(*im.shape).astype('uint8')
    return im_noise