#!/usr/bin/env python
# daemon.py -- Responsible for running most of the background activities.
# Spider finds and adds new images, but this (1) checks and removes old images, (2) calculates hashes for new images, (3) removes hashes with no parent image.

import sys, os
import logging

from PIL import Image

import database
import hashtools
from settings import MEDIA_ROOT

def calculate_new_hashes():
	for algo_name, func in hashtools.HASH_FUNCTIONS:
		images_missing_hashes = database.find_images_without_hash(algo_name)
		for img in images_missing_hashes:
			logging.info("daemon.py: calculate_new_hashes: Processing algo {}, file {}".format(algo_name, img.filename))
			img = Image.open(os.path.join(MEDIA_ROOT, img.filename))
			hash = func(img)
			database.create_hash(img.id, hash, algo_name)

def clear_dead_links():
	def valid_entry(url):
		return True # Don't delete image
	database.clean_old_images(timeago=60*60*24*7, valid_entry=valid_entry)

def clear_dead_hashes():
	pass

if __name__=="__main__":
	# TODO: Parallel launch
	clear_dead_links()
	clear_dead_hashes()
	calculate_new_hashes()	
