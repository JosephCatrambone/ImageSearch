#!/usr/bin/env python
# hashtools.py -- The daemon which sits in the background and monitors for newly added images, then adds the hashes to the database.

from hashlib import sha512
from Pillow import PIL

HASH_ALGORITHMS = {'exact':exact}

def exact(image):
	return sha512(image).digest()

def main():
	pass

if __name__=="__main__":
	main()
