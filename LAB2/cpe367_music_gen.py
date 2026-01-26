#!/usr/bin/python

import sys
import time

import base64
import random as random

import datetime
import time
import math

from cpe367_wav import cpe367_wav



############################################
############################################
# define function to add one note to list
# students - modify this function as needed!

def add_note(xlist,amp,w0,nstart,nlen,sigma):
	for n in range(nstart, nstart+nlen):
		xlist[n] += math.exp(-(n - nstart) / (sigma)) * amp * math.sin(w0 * (n - nstart))

	# note summed into signal
	return
	
			


############################################
############################################
# define routine for generating signal in WAV format
def gen_wav(fpath_wav_out):
	"""
	: this example generates a WAV file
	: output is accomplished via WAV files
	: return: True or False 
	"""
	
	# construct object for writing WAV file
	#  assign object a name, to facilitate status and error reporting
	wav_out = cpe367_wav('wav_out',fpath_wav_out)
		
	# setup configuration for output WAV
	num_channels = 1
	sample_width_8_16_bits = 16
	sample_rate_hz = 16000
	wav_out.set_wav_out_configuration(num_channels,sample_width_8_16_bits,sample_rate_hz)
		
	# open WAV output file
	ostat = wav_out.open_wav_out()
	if ostat == False:
		print('Cant open wav file for writing')
		return False
	
	
	
	###############################################################
	###############################################################
	# students - modify this section here

	# these parameters will need updating!
	#  you may also wish to add more parameters
	total_num_samples = 41040
	
	# allocate list of zeros to store an empty signal
	xlist = [0] * total_num_samples

	# setup one note
	#  this implementation does not include harmonics or a decay
	w = 2 * math.pi / sample_rate_hz
	max_amp = 32767*0.75;

	# Number of beats in the sample
	num_beats = 9;
	# Yields samples per beat
	beat_dur_samples = total_num_samples / num_beats;

	# Duration of treble and bass notes in samples
	treble_len = (beat_dur_samples)
	bass_len = (beat_dur_samples * 3)

	# Sigma values for treble and bass
	treble_sigma_base = treble_len * 0.5
	bass_sigma_base = bass_len * 0.75

	# Treble notes in sequence, first note is 0, as there is no note
	treble_notes = [ 0, 392, 440, 493.88, 587.33, 523.25, 523.25, 659.25, 587.33 ]
	# Bass notes in sequence
	bass_notes = [ 98, 196, 164.81 ]
	# Number of harmonics to generate for bass and treble
	num_treble_harmonics = 20
	num_bass_harmonics = 8
	
	# Generate each treble note
	for n_index in range(len(treble_notes)):
		# Grab the current note
		note = treble_notes[n_index]
		
		# Counter to keep track of harmonics used
		count = 0
		# Counter to keep track of how many high/low (amplitude) harmonics to generate in order
		harm_count = 1

		while count != num_treble_harmonics:
			# Generate high (amplitude) harmonics
			for __ in range(harm_count):
				add_note(
					xlist,
					(max_amp/(2*(count+1))),
					w * (count+1) * note,
					round(n_index * treble_len),
					round(treble_len),
					treble_sigma_base
				)
				count += 1

			# Generate low (amplitude) harmonics
			for __ in range(harm_count):
				add_note(
					xlist,
					(max_amp/(2*(count+1))) / 5,
					w * (count+1) * note,
					round(n_index * treble_len),
					round(treble_len),
					treble_sigma_base
				)
				count += 1

			# Increase harmonic count
			# Starts at 1: (1 high, 1 low)
			# Next is at 2: (2 high, 2 low)
			# Etc, etc. Mimics as close as possible (without hardcoding) the spectrogram of the real sample
			harm_count += 1



	# The same as above, expect for the bass notes now
	# Only other major difference is that the harmonic count starts at 4
	for n_index in range(len(bass_notes)):
		note = bass_notes[n_index]
		count = 0
		harm_count = 4
		while count != num_bass_harmonics:
			for __ in range(harm_count):
				add_note(
					xlist,
					(max_amp/(2*(count+1))),
					w * (count) * note,
					round(n_index * bass_len),
					round(bass_len),
					bass_sigma_base
				)
				count += 1
			for __ in range(harm_count):
				add_note(
					xlist,
					(max_amp/(2*(count+1))) / 5,
					w * (count) * note,
					round(n_index * bass_len),
					round(bass_len),
					bass_sigma_base 
				)
				count += 1

			harm_count += 1
	
	# students - well done!
	###############################################################
	###############################################################



	# write samples to output file one at a time
	for n in range(total_num_samples):
	
		# convert to signed int
		yout = int(round(xlist[n]))
		
		# output current sample 
		ostat = wav_out.write_wav(yout)
		if ostat == False: break
	
	# close input and output files
	#  important to close output file - header is updated (with proper file size)
	wav_out.close_wav()
		
	return True





############################################
############################################
# define main program
def main():

	# check python version!
	major_version = int(sys.version[0])
	if major_version < 3:
		print('Sorry! must be run using python3.')
		print('Current version: ')
		print(sys.version)
		return False
		
	# grab file names
	# fpath_wav_out = sys.argv[1]
	fpath_wav_out = 'music_synth.wav'

	# let's do it!
	return gen_wav(fpath_wav_out)
	
			
	
	
############################################
############################################
# call main function
if __name__ == '__main__':
	
	main()
	quit()
