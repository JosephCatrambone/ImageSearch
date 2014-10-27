#!/usr/bin/env python
# hashtools.py -- The daemon which sits in the background and monitors for newly added images, then adds the hashes to the database.

from hashlib import sha512
from Pillow import PIL
import numpy
import pickle

HASH_ALGORITHMS = {'exact':exact}

def exact(image):
	return sha512(image).digest()

#def phash(image, hash_size=32):
#	image = image.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)
#	pixels = numpy.array(image.getdata(), dtype=numpy.float).reshape((hash_size, hash_size))
#	dct = scipy.fftpack.dct(pixels)
#	dctlowfreq = dct[:8, 1:9]
#	avg = dctlowfreq.mean()
#	diff = dctlowfreq > avg
#	return ImageHash(diff)

NN = None
def nn_hash(image):
	global NN
	if NN is None:
		pass # Load NN
	#img = Image.open(filename)
	img = img.convert('L').resize((128,128))
	arr = numpy.asarray(img)
	arr = arr.reshape((1,128*128))
	_, ha, _ = NN.forward_propagate(numpy.asmatrix(arr))
	return ha

def main():
	pass
	# Sanity test

if __name__=="__main__":
	main()
