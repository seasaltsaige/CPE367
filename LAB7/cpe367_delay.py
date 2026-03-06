#!/usr/bin/python

import sys
import time
import math
import base64
import random as random
import numpy as np
import matplotlib.pyplot as plt

import datetime
import time

from cpe367_wav import cpe367_wav
from my_fifo import my_fifo


def load_samples(N: int, samps: list):
    return samps[0:N]


def calc_dft(samples: list):
    # Length of the sample list
    LEN = len(samples)
    # Row vector
    n = np.arange(LEN)
    # Column vector
    k = n.reshape((LEN, 1))
    # get the twiddles (matrix, n x k [or k x n i forget])
    e = np.exp(-2j * np.pi * k * n / LEN)
    # compute the dot product for each row to get output dft vector
    DFT = np.dot(e, samples) / LEN
    return DFT


import matplotlib.pyplot as plt
import numpy as np


def plot_spectrum(magnitude: list, fs: int, N: int):

    freqs = []
    mags = []

    for k in range(1, N // 2):

        freq = k * fs / N

        if freq > 2000:
            break

        freqs.append(freq)
        mags.append(np.abs(magnitude[k]))

    fig, ax = plt.subplots()

    ax.plot(np.array(freqs), np.array(mags))

    ax.set(xlabel="Frequency (Hz)", ylabel="Counts", title="Magnitude Spectrum")

    ax.grid()

    plt.show()


############################################
############################################
# define routine for implementing a digital filter
def process_wav(fpath_wav_in, fpath_wav_out):
    """
    : this example does not implement an echo!
    : input and output is accomplished via WAV files
    : return: True or False
    """

    # construct objects for reading/writing WAV files
    #  assign each object a name, to facilitate status and error reporting
    wav_in = cpe367_wav("wav_in", fpath_wav_in)
    # wav_out = cpe367_wav('wav_out',fpath_wav_out)

    # open wave input file
    ostat = wav_in.open_wav_in()
    if ostat == False:
        print("Cant open wav file for reading")
        return False

    # setup configuration for output WAV
    num_channels = 1
    sample_width_8_16_bits = 16
    sample_rate_hz = 8000
    # wav_out.set_wav_out_configuration(num_channels,sample_width_8_16_bits,sample_rate_hz)

    # open WAV output file
    # ostat = wav_out.open_wav_out()
    # if ostat == False:
    # 	print('Cant open wav file for writing')
    # 	return False

    ###############################################################
    ###############################################################
    # students - allocate your fifo, with an appropriate length (M)

    N = 4000

    samples = []

    xin = 0
    n = 0
    while xin != None:

        xin = wav_in.read_wav()
        if xin == None:
            break

        samples.append(xin)

        n += 1

    first = load_samples(N, samples)

    dft = calc_dft(first)
    # print(len(dft))
    plot_spectrum(dft, sample_rate_hz, len(dft))

    # 	# convert to signed int
    # 	yout = int(round(yout))

    # 	# output current sample
    # 	ostat = wav_out.write_wav(yout)
    # 	if ostat == False: break

    # # close input and output files
    # #  important to close output file - header is updated (with proper file size)
    wav_in.close_wav()
    # wav_out.close_wav()

    return True


############################################
############################################
# define main program
def main():

    # check python version!
    major_version = int(sys.version[0])
    if major_version < 3:
        print("Sorry! must be run using python3.")
        print("Current version: ")
        print(sys.version)
        return False
    if len(sys.argv) < 2:
        return print("err")

    # grab file names
    fpath_wav_in = sys.argv[1]
    # fpath_wav_out = sys.argv[2]

    if not fpath_wav_in:
        return print("Err")

    return process_wav(fpath_wav_in, "")


if __name__ == "__main__":

    main()
    quit()
