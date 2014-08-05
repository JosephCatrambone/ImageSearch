#!/usr/bin/env python
# spider.py -- The job which browses pages in the background, pulls images, and pushes them into the database.
# Credit to Jake Austwick for an awesome scraper writeup which improved the accuracy and performance of this scraper ten-fold.
# If lxml is not installing, aptitide install libxml2-dev libxslt-dev python-dev lib32z1-dev

import sys, os
import requests
from lxml import html
import urlparse
import collections
import cPickle as pickle # TODO: Some sites may have maliciously crafted URLs which can break pickle, possible?
import time

FREEZE_FILE = "spider.pkl"
STARTING_PAGE = "http://josephcatrambone.com"
MEDIA_FOLDER = "./images/"

def save_state(state_vars, freeze_file=FREEZE_FILE):
	fout = open(freeze_file, 'wb')
	pickle.dump(state_vars, fout, pickle.HIGHEST_PROTOCOL)
	fout.close()

def restore_state(freeze_file=FREEZE_FILE):
	try:
		fin = open(freeze_file, 'rb')
		state = pickle.load(fin)
		fin.close()
	except IOException as ioe:
		return None
	return state

def main():
	# Set up initial state
	url_queue = collection.deque()
	visited_urls = set()
	url_queue.append(STARTING_PAGE)

	# Quick restore else save
	last_state = restore_state()
	if last_state:
		url_queue, visited_urls = last_state
	else:
		save_state((url_queue, visited_urls))

	# Begin main search loop
	while len(url_queue):
		url = url_queue.popleft()
		if url in visited_urls:
			continue

		# Get the page
		response = requests.get(url)
		parsed_body = html.fromstring(response.content)

		# Find URLs
		outbound_urls = [urlparse.urljoin(response.url, url) for url in parsed_body.xpath('//a/@href')]
		image_urls = [urlparse.urljoin(response.url, url) for url in parsed_body.xpath('//img/@src')]

		# Handle the URLs
		for new_url in outbound_urls:
			if new_url.startswith('http'):
				url_queue.append(new_url)
		for image in image_urls:
			img_response = requests.get(image)
			fout = open(os.path.join(MEDIA_FOLDER, image.split('/')[-1]), 'w') # TODO: Hash filename
			fout.write(r.content)
			fout.close()

		# Mark this as complete and save our state
		visited_urls.add(url)
		save_state((url_queue, visited_urls))

		# Throttle
		time.sleep(1)

if __name__=="__main__":
	main()
