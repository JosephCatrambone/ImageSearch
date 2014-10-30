#!/usr/bin/env python
# daemon.py -- Responsible for running most of the background activities.
# Spider finds and adds new images, but this (1) checks and removes old images, (2) calculates hashes for new images, (3) removes hashes with no parent image.

import sys, os
import logging

from PIL import Image
import requests

import database
import hashtools
from settings import MEDIA_ROOT

def calculate_new_hashes():
	for algo_name, func in hashtools.HASH_ALGORITHMS.iteritems():
		images_missing_hashes = database.get_images_without_hash(algo_name)
		for image_row in images_missing_hashes:
			logging.info("daemon.py: calculate_new_hashes: Processing algo {}, file {}".format(algo_name, image_row['filename']))
			image = Image.open(os.path.join(MEDIA_ROOT, image_row['filename']))
			hash = func(image)
			database.create_hash(image_row['id'], hash, algo_name)

def clear_dead_links():
	old_images = database.get_old_images(timeago=60*60*24*7)
	broken_image_ids = list()
	for img in old_images:
		pass # TODO: URL Check for 404
	if len(broken_image_ids) > 0:
		database.delete_images(broken_image_ids)

if __name__=="__main__":
	# TODO: Parallel launch
	clear_dead_links()
	calculate_new_hashes()	
