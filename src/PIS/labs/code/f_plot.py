# f_plot.py

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as m_io

import librosa
import librosa.display

import IPython.display as ipd

from skimage.color import rgb2gray

import PIL

from scipy import signal, fftpack, interpolate
from scipy.fft import fft, ifft

### PLOT IMAGENES

def is_pil_image(im):
    return isinstance(im, PIL.Image.Image)

##

def plot_im(im, titulo = None, fsize = 14):
    """ Plot an image

    Args: 
        im: image   
        titulo: title
        fsize: size of title
    """
    
    if is_pil_image(im):
        plt.imshow(im)
    else:        
        if im.ndim == 2:
            plt.imshow(im, cmap=plt.cm.gray)
        else:
            plt.imshow(im)
    plt.set_title(titulo, fontsize=fsize)
    plt.set_axis_off()
    plt.show()

##

def plotN_im(l_im, ncols = 1, l_tit = None, fsize = 14):
    """Plot several images (side by side)
      
    Args: 
        lista_im: list of images
        ncols: number of columns   
        lista_tit: list of titles
        fsize: size of title
    """
    n_im = len(l_im)
    if l_tit is None: 
        l_tit = ['Image (%d)' % i for i in range(1, n_im + 1)]
    nrows = int(np.ceil(n_im/float(ncols)))
    
    fig = plt.figure(figsize=(ncols*7, nrows*7))
    #fig = plt.figure(layout="constrained")
    for n, (im, titulo) in enumerate(zip(l_im, l_tit)):
        ax = fig.add_subplot(nrows, ncols, n + 1)
        if is_pil_image(im):
            ax.imshow(im)
        else:    
            if im.ndim == 2:
            	ax.imshow(im, cmap=plt.cm.gray)
            else:
            	ax.imshow(im)
        ax.set_title(titulo, fontsize=fsize)
        ax.set_axis_off()
    #fig.set_size_inches(np.array(fig.get_size_inches()) * n_im)
    plt.subplots_adjust(hspace=0.05, wspace=0.05)
    plt.show()

##

def plot_im_read(n_im, titulo = None, fsize = 14):
    """Plot an image
      
    Args: 
        n_im: name of image   
        titulo: title
        fsize: size of title
    """
    im = m_io.imread(n_im)
    if im.ndim == 2:
        plt.imshow(im, cmap=plt.cm.gray)
    else:
        plt.imshow(im)
    plt.set_title(titulo, fontsize=fsize)
    plt.set_axis_off()
    plt.show()

##

def plotN_im_read(l_im, ncols = 1, l_tit = None, fsize = 14):
    """Read and plot several images (side by side)
      
    Args: 
        l_im : list of images (names)
        ncols: number of columns   
        l_tit: list of titles
        fsize: size of title
    """
    n_im = len(l_im)

    if l_tit is None: 
        l_tit = ['Image (%d)' % i for i in range(1, n_im + 1)]

    fig = plt.figure()
    for n, (name_image, titulo) in enumerate(zip(l_im, l_tit)):
        ax = fig.add_subplot(int(np.ceil(n_im/float(ncols))), ncols, n + 1)
        imagen = m_io.imread(name_image)
        if imagen.ndim == 2:
            plt.gray()
        ax.imshow(imagen)
        ax.set_title(titulo, fontsize=fsize)
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_im)
    plt.show()

##

def plot2_im(im1, im2):
    # Plot two images
    image1 = m_io.imread(im1)
    image2 = m_io.imread(im2)

    fig, (ax1,ax2) = plt.subplots(nrows=1,ncols=2,figsize=(15,10))
    ax1.imshow(image1)
    ax2.imshow(image2)

    plt.tight_layout()
    plt.show()

##

def plot2_im_gray(im, im_gray=None):
    """ 1. Plot the original image (RGB)
        2. Plot grayscale image
    Args: 
        im: image (RGB)
        im_gray: grayscale image
    """
    if im_gray is None:
        im_gray = rgb2gray(im)

    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    axs = axes.ravel()
    axs[0].imshow(im)
    axs[0].set_title("Original")
    axs[0].set_axis_off()
    axs[1].imshow(im_gray, cmap=plt.cm.gray)
    axs[1].set_title("Grayscale")
    axs[1].set_axis_off()
    fig.tight_layout()
    plt.show()

###########################################
## Senales y espectros
###########################################

def plot_ss(x, fs=44100, w_name = 'hann', w_size = 2048, w_ovlp = 1024, fmin=0, fmax=22050, titulo=None):
    """ 1. Plot spectrum of signal
        2. Plot spectrogram of signal
    Args: 
        x: input signal
        fs: sampling rate of x
        w_name: window name (default: 'hann', Hanning window)
        w_size: window length
        w_ovlp: window overlap
        fmin: minimum Frequency (to display)
        fmax: maximum Frequency (to display)
        titulo: title of figure
    """
    S = np.abs(librosa.stft(x, window=w_name, n_fft=w_size, hop_length=w_ovlp))
    D = librosa.amplitude_to_db(S, ref=np.max)
    f = np.linspace(0, fs/2,num=len(S))

    fig, axs = plt.subplots(ncols=3, figsize=(8, 4), sharex=False, sharey=False)
    axs[0].plot(f/1000, S)
    axs[0].set_title(titulo+' Spectrum')
    axs[0].set_xlabel('Frequency (kHz)')
    axs[0].set_ylabel('Magnitude')
    axs[1].specgram(x, Fs=fs)
    axs[1].set_title(titulo+' Spectrogram')
    axs[1].set_xlabel('Time(s)')
    axs[1].set_ylabel('Frequency (kHz)')
    librosa.display.specshow(D, sr=fs, n_fft= w_size, fmin = fmin, fmax = fmax, ax=axs[2])
    fig.tight_layout()
    plt.show()

##

def plot_new_ss(x, fs=44100, w_name = 'hann', w_size = 2048, w_ovlp = None, titulo=None):
    """ 1. Plot spectrum of signal
        2. Plot spectrogram of signal
        3. Plot constant-Q power spectrum of signal
      
    Args: 
        x: Input signal
        fs: Sampling rate of x
        w_name: Window name (default: 'hann', Hanning window)
        w_size: Window length
 	    w_ovlp: Window overlap
        titulo: Title of figure
    """
    if w_ovlp == None:
        w_ovlp = w_size // 4

    fmin = librosa.note_to_hz('C2')
    fmax = librosa.note_to_hz('C6')

    S = np.abs(librosa.stft(x, window=w_name, n_fft=w_size, hop_length=w_ovlp))
    S_db = librosa.amplitude_to_db(S, ref=np.max)

    C = np.abs(librosa.cqt(x, sr=fs, window=w_name, hop_length=w_ovlp, 
                            fmin=librosa.note_to_hz('C2'), n_bins=60*2, bins_per_octave=12*2))
    C_db = librosa.amplitude_to_db(C, ref=np.max)

    fig, axs = plt.subplots(ncols=3, figsize=(15, 5), tight_layout=True)
    #f = np.linspace(0, fs/2, num=len(S))
    #axs[0].plot(f/1000, S)
    axs[0].magnitude_spectrum(x, color ='blue')
    axs[0].set_title(titulo+' Spectrum')
    axs[0].set_xlabel('Frequency (kHz)')
    axs[0].set_ylabel('Magnitude')
    librosa.display.specshow(S_db, sr=fs, x_axis='time', y_axis="log", n_fft = w_size, fmin=fmin, fmax=fmax, ax=axs[1])
    axs[1].set_title(titulo+' Spectrogram')
    librosa.display.specshow(C_db, sr=fs, y_axis="cqt_note", n_fft=w_size, fmin=fmin, fmax=fmax, ax=axs[2])
    axs[2].set_title(titulo+' Constant-Q power spectrum')
    plt.show()

##

def plotN_ss(l_x, l_fs, l_tit = None, fs=44100, w_name = 'hann', w_size = 2048, w_ovlp = 1024, fmin=0, fmax=22050, titulo=None):
    """ 1. Plot spectrum of signal
        2. Plot spectrogram of signal
    Args: 
        x: List of input signals
        fs: List of sampling rate of x    
        titulo: List of titles
        w_name: window name (default: 'hann', Hanning window)
	    w_size: window length
	    w_ovlp: window overlap
	    fmin: minimum Frequency (to display)
	    fmax: maximum Frequency (to display)
    """
    n_x = len(l_x)
    if l_tit is None: 
        l_tit = ['(%d)' % i for i in range(1, n_x + 1)]

    fig, axs = plt.subplots(nrows=n_x, ncols=3, figsize=(n_x*7, n_x*4), sharex=False, sharey=False)

    for i in range(0, n_x):
        x   = l_x[i]
        fs  = l_fs[i]
        t_x = l_tit[i]
        S = np.abs(librosa.stft(x, window=w_name, n_fft=w_size, hop_length=w_ovlp))
        D = librosa.amplitude_to_db(S, ref=np.max)
        f = np.linspace(0, fs/2,num=len(S))

        axs[i,0].plot(f/1000, S)
        axs[i,0].set_title(t_x+': Spectrum')
        axs[i,0].set_xlabel('Frequency (kHz)')
        axs[i,0].set_ylabel('Magnitude')
        axs[i,1].specgram(x, Fs=fs)
        axs[i,1].set_title(t_x+': Spectrogram')
        axs[i,1].set_xlabel('Time(s)')
        axs[i,1].set_ylabel('Frequency (kHz)')
        librosa.display.specshow(D, sr=fs, n_fft= w_size, fmin = fmin, fmax = fmax, ax=axs[i,2])
    
    fig.tight_layout()
    plt.show()

##

def plotN_wss_old(l_x, fs, l_t = None, l_tit = None):
    """ 1. Plots the waveform of signals
        2. Plot spectrum of signals
        3. Plot spectrogram of signals
      
    Args: 
        lista_x: List of input signals  
        lista_tit: List of titles
        fs: Sampling rate
    """
    n_x = len(l_x)
    if l_tit is None: 
        l_tit = ['(%d)' % i for i in range(1, n_x + 1)]

    fig, axs = plt.subplots(nrows=n_x, ncols=3, figsize=(n_x*7, n_x*4), sharex=False, sharey=False)

    for i in range(0, n_x):
        x = l_x[i]
        S = np.abs(librosa.stft(x))
        f = np.linspace(0, fs/2, num=len(S))

        if l_t is None:
            axs[0,i].plot(x)
        else:
            if isinstance(l_t, list):
                axs[0,i].plot(l_t[i], x)
            else:
                axs[0,i].plot(l_t, x)

        axs[i,0].set_title(l_tit[i])
        axs[i,0].set_xlabel('Time(s)')
        axs[i,0].set_ylabel('Amplitude')
        axs[i,1].plot(f/1000, S)
        axs[i,1].set_title('Spectrum')
        axs[i,1].set_xlabel('Frequency (kHz)')
        axs[i,1].set_ylabel('Magnitude')
        axs[i,2].specgram(x, Fs=fs)
        axs[i,2].set_title('Spectrogram')
        axs[i,2].set_xlabel('Time(s)')
        axs[i,2].set_ylabel('Frequency (kHz)')
    
    fig.tight_layout()
    plt.show()

##

def plotN_wss(l_x, l_fs, l_tit = None):
    """ 1. Plots the waveform of signals
        2. Plot spectrum of signals
        3. Plot spectrogram of signals
    Args: 
        l_x: List of input signals
        l_fs: List of sampling rate  
        titulo: List of titles
    """
    n_x = len(l_x)
    if l_tit is None: 
        l_tit = ['(%d)' % i for i in range(1, n_x + 1)]

    fig, axs = plt.subplots(nrows=n_x, ncols=3, figsize=(n_x*7, n_x*4), sharex=False, sharey=False)
    for i in range(0, n_x):
        x   = l_x[i]
        fs  = l_fs[i]
        t_x = l_tit[i]
        S = np.abs(librosa.stft(x))
        f = np.linspace(0, fs/2, num=len(S))
        axs[i,0].plot(x)
        axs[i,0].set_title(t_x)
        axs[i,0].set_xlabel('Time(s)')
        axs[i,0].set_ylabel('Amplitude')
        axs[i,1].plot(f/1000, S)
        axs[i,1].set_title('Spectrum')
        axs[i,1].set_xlabel('Frequency (kHz)')
        axs[i,1].set_ylabel('Magnitude')
        axs[i,2].specgram(x, Fs=fs)
        axs[i,2].set_title('Spectrogram')
        axs[i,2].set_xlabel('Time(s)')
        axs[i,2].set_ylabel('Frequency (kHz)')
    fig.tight_layout()
    plt.show()

##

def plotN_wss_db(l_x, fs, l_t = None, ref=32768, l_tit=None):
    """ 1. Plots the waveform of signals
        2. Plot spectrum of signals
        3. Plot spectrogram of signals (dB)
      
    Args: 
        l_x: List of input signals
        t: time steps
        fs: sampling rate
        l_tit: List of titles
    """
    n_x = len(l_x)
    if l_tit is None: 
        l_tit = ['(%d)' % i for i in range(1, n_x + 1)]
    
    fig, axs = plt.subplots(nrows=2, ncols=n_x, figsize=(n_x*7, n_x*4), sharex=False, sharey=False)
    
    for i in range(0, n_x):
        #X = np.fft.rfft(lista_x[i])
        #freqs = np.arange((N/2) + 1) / (float(N)/fs)
        #s_mag = np.abs(X)*2.0/N
        #s_dbfs = 20.0*np.log10(s_mag/ref)
        #plt.plot(freqs, s_dbfs)

        #S = np.abs(librosa.stft(x))
        #S_db = librosa.amplitude_to_db(S, ref=np.max)
        #f = np.linspace(0, fs/2, num=len(S))
        #plt.plot(t, x)
        #plt.plot(f/1000, S)

        N = len(l_x[i])
        X = np.fft.rfft(l_x[i])
        freqs = np.arange((N / 2) + 1) / (float(N) / fs)
        
        # Scale the magnitude of FFT by window and factor of 2,
        # because we are using half of FFT spectrum.
        s_mag = np.abs(X) * 2.0 / N
        # Convert to dBFS
        s_dbfs = 20.0 * np.log10(s_mag/ref)
        
        if l_t is None:
            axs[0,i].plot(l_x[i], 'r')
        else:
            if isinstance(l_t, list):
                axs[0,i].plot(l_t[i], l_x[i], 'r')
            else:
                axs[0,i].plot(l_t, l_x[i], 'r')

        axs[0,i].set_xlabel('Time(s)')
        axs[0,i].set_ylabel('Amplitude')
        axs[0,i].set_title(l_tit[i])
        
        axs[1,i].plot(freqs, s_dbfs)
        axs[1,i].set_xlabel('Frequency [Hz]')
        axs[1,i].set_ylabel('Magnitude(db)')
        axs[1,i].set_title('Spectrum')

    fig.tight_layout()
    plt.show()

def plotN_wss_stem(l_x, fs, l_t = None):
    """ 1. Plots the waveform of signals (with stems)
        2. Plot spectrum of signals
        3. Plot spectrogram of signals
      
    Args: 
        lista_x: List of input signals
        fs: Sampling rate
        t: time steps
    """
    n_x = len(l_x)
    fig, axs = plt.subplots(nrows=2, ncols=n_x, figsize=(n_x*7, n_x*4), sharex=False, sharey=False)

    for i in range(0, n_x):
        N = len(l_x[i])

        if l_t is None:
            axs[0,i].plot(l_x[i], 'r')
        else:
            if isinstance(l_t, list):
                axs[0,i].plot(l_t[i], l_x[i], 'r')
            else:
                axs[0,i].plot(l_t, l_x[i], 'r')

        axs[0,i].set_xlabel('Time(s)')
        axs[0,i].set_ylabel('Amplitude')
        
        X = fftpack.fft(l_x[i])
        freqs = fftpack.fftfreq(N)*fs
        
        axs[1,i].stem(freqs, np.abs(X))
        axs[1,i].set_xlabel('Frequency [Hz]')
        axs[1,i].set_ylabel('Magnitude')
        axs[1,i].set_xlim(-fs/2.0, fs/2.0)
        axs[1,i].set_ylim(-5, 110)
    
    fig.tight_layout()
    plt.show()

##

def plot_ws_mag_ph(l_x, l_t=None):
    ######################################
    # Plot señal + magnitud + fase
    ######################################

    n_x = len(l_x)

    fig, axs = plt.subplots(nrows=3, ncols=n_x, figsize=(n_x*7, n_x*4), sharex=False, sharey=False)
    for i in range(0, n_x):
        N = len(l_x[i])

        if l_t is None:
            axs[0, i].plot(l_x[i], 'r')
        else:
            if isinstance(l_t, list):
                axs[0, i].plot(l_t[i], l_x[i], 'r')
            else:
                axs[0, i].plot(l_t, l_x[i], 'r')

        axs[0, i].set_xlabel('Time(s)')
        axs[0, i].set_ylabel('Amplitude')
        # Magnitud espectral en dB
        axs[1, i].magnitude_spectrum(l_x[i], color='green')
        axs[2, i].phase_spectrum(l_x[i], color ='blue') 
    fig.tight_layout()
    plt.show()

##

def plot2_wss_db_join(s, t, ss, ts, fs=1, ref=32768):
    X1 = fft(s)
    N = len(X1)
    n = np.arange(N)
    T = N/fs
    freqs = n/T

    X2 = np.fft.rfft(s)
    freqs = np.arange(N/2) / (float(N) / fs)
    #freqs = np.arange((N / 2) + 1) / (float(N) / fs)
    s_mag = np.abs(X2) * 2.0 / N
    s_dbfs = 20.0 * np.log10(s_mag/ref)

    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(21, 4), sharex=False, sharey=False)
    axs[0].plot(t, s, 'r*')
    axs[0].plot(ts, ss, 'b')
    axs[0].set_xlabel('Time(s)')
    axs[0].set_ylabel('Amplitude')
    axs[1].plot(freqs, np.abs(X1))
    axs[1].set_xlabel('Frequency [Hz]')
    axs[1].set_ylabel('Magnitude')
    axs[1].set_xlim(0, fs/2.0)    
    axs[2].plot(freqs, s_dbfs)
    axs[2].set_xlabel('Frequency [Hz]')
    axs[2].set_ylabel('Magnitude(db)')
    fig.tight_layout()
    plt.show()

##

def plotN_spectro(l_y, l_fs, ncols = 1, l_tit = None):
    n_x = len(l_y)
    if l_tit is None: 
        l_tit = ['Function (%d)' % i for i in range(1, n_x + 1)]

    fig = plt.figure()
    for n, (fs, y, titulo) in enumerate(zip(l_fs, l_y, l_tit)):
        ax = fig.add_subplot(int(np.ceil(n_x/float(ncols))), ncols, n + 1)

        X = librosa.stft(y, hop_length=128)
        D = librosa.amplitude_to_db(np.abs(X), ref=np.max)

        specshow(D, sr=fs, x_axis='log', y_axis='hz', hop_length=128, bins_per_octave=24)

        ax.set_xlabel('Time(s)')
        ax.set_ylabel('Frequency (kHz)')
        ax.set_title(titulo)
        ax.grid(True)
        #ax.set_ylim(top=12000)
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_x)
    plt.colorbar()
    #plt.grid(True)
    plt.show()

##

def plot_FIR_filter_spec(*args, title='', dB=False, func='plot'):
    
    if len(args)==1:
        x=args[0]
    else:
        f_step=args[0]
        x=args[1]
    
    mag = np.real(np.sqrt(x * np.conj(x)))
    phase = np.arctan2(np.imag(x), np.real(x))
    phase = np.unwrap(phase)
    
    fig, axs = plt.subplots(2, 1)
    
    mag_ylabel = 'Magnitude [dB]'
    xlabel='Frequency [Hz]'
    
    if dB is True:
        mag = 20*np.log10(mag)
        mag_ylabel = 'Magnitude [dB]'
    
    if len(args)==1:
        xlabel='Frequency [k]'
        eval('axs[0].'+func+'(mag)')
        axs[1].plot(phase)
    else:
        eval('axs[0].'+func+'(f_step, mag)')
        axs[1].plot(f_step, phase)
        
    axs[0].set(xlabel=xlabel, ylabel=mag_ylabel, title=title)
    axs[1].set(xlabel=xlabel, ylabel='Phase [radians] ')
    axs[0].grid()
    axs[1].grid()
    fig.tight_layout()
    
    return plt

## IMAGEN + COLOR

def plotRGB_channels(rgb):
    fig, axs = plt.subplots(2, 3, figsize=(12, 6))
    axs[0, 0].axis(False)
    axs[0, 1].imshow(rgb)
    axs[0, 1].axis(False)
    axs[0, 2].axis(False)
    axs[1, 0].imshow(rgb[:,:,0], cmap='Reds', vmin=0, vmax=255)
    axs[1, 0].set_title("R")
    axs[1, 0].axis(False)
    axs[1, 1].imshow(rgb[:,:,1], cmap='Greens', vmin=0, vmax=255)
    axs[1, 1].set_title("G")
    axs[1, 1].axis(False)
    axs[1, 2].imshow(rgb[:,:,2], cmap='Blues', vmin=0, vmax=255)
    axs[1, 2].set_title("B")
    axs[1, 2].axis(False)

##

def plotCMYK_channels(cmyk, mapas_colores):
    fig, axs = plt.subplots(2, 3, figsize=(12, 6))
    axs[0, 0].axis(False)
    axs[0, 1].set_title("K")
    axs[0, 1].imshow(cmyk[:,:,3], cmap=plt.cm.gray)
    axs[0, 1].axis(False)
    axs[0, 2].axis(False)
    axs[1, 0].imshow(cmyk[:,:,0], cmap=mapas_colores[0], vmin=0, vmax=255)
    axs[1, 0].set_title("R")
    axs[1, 0].axis(False)
    axs[1, 1].imshow(cmyk[:,:,1], cmap=mapas_colores[1], vmin=0, vmax=255)
    axs[1, 1].set_title("G")
    axs[1, 1].axis(False)
    axs[1, 2].imshow(cmyk[:,:,2], cmap=mapas_colores[2], vmin=0, vmax=255)
    axs[1, 2].set_title("B")
    axs[1, 2].axis(False)

##

def plot2_RGB_gray(original, grayscale):
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    axs = axes.ravel()

    axs[0].imshow(original)
    axs[0].set_title("Original")
    axs[0].set_axis_off()
    axs[1].imshow(grayscale, cmap=plt.cm.gray)
    axs[1].set_title("Grayscale")
    axs[1].set_axis_off()

    fig.tight_layout()
    plt.show()

##

def plot4(i1, i2, i3, i4, c1=None, c2=None, c3=None, c4=None):
    fig, axs = plt.subplots(nrows=2,ncols=2,figsize=(15,10))
    axs[0, 0].set_title(c1)
    axs[0, 0].imshow(i1)
    axs[0, 0].set_axis_off()
    axs[0, 1].set_title(c2)
    axs[0, 1].imshow(i2)
    axs[0, 1].set_axis_off()
    axs[1, 0].set_title(c3)
    axs[1, 0].imshow(i3)
    axs[1, 0].set_axis_off()
    axs[1, 1].set_title(c4)
    axs[1, 1].imshow(i4)
    axs[1, 1].set_axis_off()
    plt.show()

### SENAL DE AUDIO

def print_plot_play(x, fs, text=''):
    """ 1. Prints information about an audio signal 
        2. Plots the waveform
        3. Creates player
      
    Args: 
        x: input signal
        fs: sampling rate of x    
        text: text to print
    """
    print('%s Fs = %d, x.shape = %s, x.dtype = %s' % (text, fs, x.shape, x.dtype))
    plt.figure(figsize=(8, 2))
    plt.plot(x, color='gray')
    plt.xlim([0, x.shape[0]])
    plt.xlabel('Time (samples)')
    plt.ylabel('Amplitude')
    plt.tight_layout()
    plt.show()
    ipd.display(ipd.Audio(data=x, rate=fs))

def plot_oscilograma(x, fs, titulo=""):
    """1. Plot oscilogram 
      
    Args: 
        x: function to plot
        fs: sampling rate
        titulo: title of plot
    """
    fig, ax = plt.subplots(figsize=(6, 3))
    librosa.display.waveshow(x, sr=fs, ax=ax, color='b')
    ax.set_title(titulo)
    ax.set_xlabel('Time(s)')
    ax.set_ylabel('Amplitude')

    fig.tight_layout()
    plt.show()

def plotN_oscilograma(l_x, l_fs, ncols = 1, l_tit = None):
    n_x = len(l_x)
    if l_tit is None: 
    	l_tit = ['Function (%d)' % i for i in range(1, n_x + 1)]
    
    fig = plt.figure()
    for n, (fs, x, titulo) in enumerate(zip(l_fs, l_x, l_tit)):
        ax = fig.add_subplot(int(np.ceil(n_x/float(ncols))), ncols, n + 1)
        librosa.display.waveshow(x, sr=fs, ax=ax, color='b')
        ax.set_xlabel('Time(s)')
        ax.set_ylabel('Amplitude')
        ax.set_title(titulo)

    fig.set_size_inches(np.array(fig.get_size_inches()) * n_x)
    plt.show()

def plot_espectrograma(x, fs, w = 2048, wn='hann', titulo=None):
    S = np.abs(librosa.stft(x, n_fft=w, window=wn))
    D = librosa.amplitude_to_db(S, ref=np.max)
    
    fig, ax = plt.subplots(figsize=(8, 4))
    xx = librosa.display.specshow(D, n_fft=w, x_axis='time', y_axis='linear', sr=fs, ax=ax)
    ax.set_title(titulo+', '+str(w)+', '+wn+', spectrogram')
    fig.colorbar(xx, ax=ax, format="%+2.f dB")
    fig.tight_layout()
    plt.show()

def plot_espectrograma_voz(x, fs, lista_w = [2048], lista_wn = ['hann'], titulo=None):
    nrows = len(lista_w)
    ncols = len(lista_wn)

    combinaciones = list(itertools.product(lista_w, lista_wn))

    fig, axs = plt.subplots(nrows, ncols)
    fig.suptitle(titulo, fontsize=24)

    for ax, a in zip(axs.flat, combinaciones):
        (w, wn) = a
        S = np.abs(librosa.stft(x, n_fft=w, window=wn))
        D = librosa.amplitude_to_db(S, ref=np.max)
        xx = librosa.display.specshow(D, n_fft=w, x_axis='time', y_axis='linear', sr=fs, ax=ax)
        #fig.colorbar(xx, ax=ax, format="%+2.f dB")
        ax.set_title(str(w)+', '+wn+', spectrogram', fontsize=12)
        ax.label_outer()

    fig.set_size_inches(np.array(fig.get_size_inches()) * nrows, forward=True)
    #fig.colorbar(xx, ax=axs, orientation='horizontal', fraction=.1, format="%+2.f dB")
    #plt.subplots_adjust(hspace=0.5)
    plt.show()

def plotN_espectrograma(l_x, l_fs, ncols = 1, l_tit = None):
    """ 1. Plot oscilogram
        2. Plot spectrogram
      
    Args: 
        x: function to plot
        fs: sampling rate
        desde, hasta: range (plot)
        titulo: title of plot
    """
    n_x = len(l_x)
    if l_tit is None: 
        l_tit = ['Function (%d)' % i for i in range(1, n_x + 1)]

    fig = plt.figure()
    for n, (fs, x, titulo) in enumerate(zip(l_fs, l_x, l_tit)):
        ax = fig.add_subplot(int(np.ceil(n_x/float(ncols))), ncols, n + 1)
        plt.specgram(x, Fs=fs)
        ax.set_xlabel('Time(s)')
        ax.set_ylabel('Frequency (kHz)')
        ax.set_title(titulo)
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_x)
    plt.show()

##

def plot_espectro(x, fs, t=None):
    S = np.abs(librosa.stft(x))
    D = librosa.amplitude_to_db(S, ref=np.max)
    f = np.linspace(0, fs/2,num=len(S))
    
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(8, 4), sharex=False, sharey=False)
    ax.plot(f/1000, S)
    ax.set_title(t+' Spectrum')
    ax.set_xlabel('Frequency (kHz)')
    ax.set_ylabel('Magnitude')

    fig.tight_layout()
    plt.show()

def plotN_espectro(l_x, l_fs, ncols = 1, l_tit = None):
    n_x = len(l_x)
    if l_tit is None: 
    	l_tit = ['Function (%d)' % i for i in range(1, n_x + 1)]
    fig = plt.figure()
    for n, (fs, x, titulo) in enumerate(zip(l_fs, l_x, l_tit)):
        ax = fig.add_subplot(int(np.ceil(n_x/float(ncols))), ncols, n + 1)

        S = np.abs(librosa.stft(x))
        D = librosa.amplitude_to_db(S, ref=np.max)
        f = np.linspace(0, fs/2,num=len(S))

        ax.set_title(titulo+' Spectrum')
        ax.plot(f/1000, S)
        ax.set_xlabel('Frequency (kHz)')
        ax.set_ylabel('Magnitude')
       
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_x)
    plt.show()

### FUNCTION AND FILTER

def plot2_of(t, data, data_f, n = "Original Signal", n_f="Filtered Signal"):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3), sharex=True, sharey=True)
    ax1.plot(t, data)
    ax1.set_title(n)
    ax1.margins(0, .1)
    ax1.grid(alpha=.5, ls='--')
    ax2.plot(t, data_f)
    ax2.set_title(n_f)
    ax2.grid(alpha=.5, ls='--')

    fig.tight_layout()
    plt.show()

### OTHER FUNCTIONS

def plot1_oo(t1, y1, t2, y2, titulo=""):
    plt.plot(t1, y1, 'b-')
    plt.plot(t2, y2, 'r-')
    plt.title(titulo)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.grid(True, which='both')
    
    plt.tight_layout()
    plt.show()

##

def plot_function(t, y, titulo=None, xticks_rotation=None, y0_color=None):
    """ 1. Plot function
      
    Args: 
        t: time
        y: function to plot
        titulo: title of plot
        xticks_rotation=None, "vertical", "horizontal"
        y0_color: color of y=0 (None or a color, 'r', 'g')
    """
    if titulo is None:
        titulo = " "

    plt.plot(t, y)
    plt.title(titulo)
    if xticks_rotation is None:
        xticks_rotation="horizontal"
    plt.xticks(rotation=xticks_rotation)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.grid(True, which='both')
    if not (y0_color is None):
        plt.axhline(y=0, color=y0_color)
    plt.tight_layout()
    plt.show()

##

def plot_function_stem(t, y, titulo=None):
    """1. Plot function with stem
      
    Args: 
        t: time
        y: function to plot
        titulo: title of plot
    """
    if titulo is None:
        titulo = " "
    
    plt.stem(t, y)
    plt.title(titulo)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.grid(True, which='both')
    plt.tight_layout()
    plt.show()

def plotN_spectro_stem(l_s, fs=22050):
    l = len(l_s)
    
    fig, axs = plt.subplots(nrows=1, ncols=l, figsize=(l*7, 4), sharex=False, sharey=False)
    for i in range(0, l):
        N = len(l_s[i])
        X = fftpack.fft(l_s[i])
        freqs = fftpack.fftfreq(N)*fs
        
        axs[i].stem(freqs, np.abs(X))
        axs[i].set_xlabel('Frequency [Hz]')
        axs[i].set_ylabel('Magnitude')
        axs[i].set_xlim(-fs/2.0, fs/2.0)
        axs[i].set_ylim(-5, 110)
    fig.tight_layout()
    plt.show()

##

def plotN_function_symbol(l_t, l_f, ncols = 1, l_tit = None, l_s = None):
    n_f = len(l_f)

    if l_tit is None: 
        l_tit = ['Function (%d)' % i for i in range(1, n_f + 1)]
    if l_s is None: 
        l_s = ['b-' % i for i in range(1, n_f + 1)]

    fig = plt.figure()
    for n, (t, x, titulo, simbolo) in enumerate(zip(l_t, l_f, l_tit, l_s)):
        ax = fig.add_subplot(int(np.ceil(n_f/float(ncols))), ncols, n + 1)
        plt.plot(t, x, simbolo)
        ax.set_title(titulo)
        ax.set_xlabel('Time(s)')
        ax.set_ylabel('Amplitude')
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_f)
    plt.show()

##

def plotN_function(l_t, l_f, ncols = 1, l_tit = None):
    n_f = len(l_f)
    if l_tit is None: 
        l_tit = ['Function (%d)' % i for i in range(1, n_f + 1)]

    fig = plt.figure()
    for n, (t, x, titulo) in enumerate(zip(l_t, l_f, l_tit)):
        ax = fig.add_subplot(int(np.ceil(n_f/float(ncols))), ncols, n + 1)
        plt.plot(t, x)
        ax.set_title(titulo)
        ax.set_xlabel('Time(s)')
        ax.set_ylabel('Amplitude')
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_f)
    plt.show()

####################

def plot_ws1(x, fs, desde=1, hasta=None, titulo=""):
    """ 1. Plot oscilogram 
        2. Plot spectrum
      
    Args: 
        x: function to plot
        fs: sampling rate
        desde, hasta: range (plot)
        titulo: title of plot
    """
    if hasta == None:
        hasta = len(x)

    S = np.abs(librosa.stft(x))
    f = np.linspace(0, fs/2, num=len(S))

    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4), sharex=False, sharey=False)
    ax1.plot(x[desde:hasta])
    ax1.set_title(titulo)
    ax1.set_xlabel('Time(s)')
    ax1.set_ylabel('Amplitude')

    ax2.plot(f/1000, S)
    ax2.set_title('Spectrum')
    ax2.set_xlabel('Frequency (kHz)')
    ax2.set_ylabel('Magnitude')
    fig.tight_layout()
    plt.show()


def plot_ws2(x, fs, desde=1, hasta=None, titulo=""):
    """ 1. Plot oscilogram 
        2. Plot spectrogram
      
    Args: 
        x: function to plot
        fs: sampling rate
        desde, hasta: range (plot)
        titulo: title of plot
    """
    if hasta == None:
        hasta = len(x)

    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4), sharex=False, sharey=False)
    ax1.plot(x[desde:hasta])
    ax1.set_title(titulo)
    ax1.set_xlabel('Time(s)')
    ax1.set_ylabel('Amplitude')
    ax2.specgram(x, Fs=fs)
    ax2.set_title('Spectrogram')
    ax2.set_xlabel('Time(s)')
    ax2.set_ylabel('Frequency (kHz)')
    fig.tight_layout()
    plt.show()
