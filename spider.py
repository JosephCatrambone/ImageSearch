#!/usr/bin/env python
# spider.py -- The job which browses pages in the background, pulls images, and pushes them into the database.
# Credit to Jake Austwick for an awesome scraper writeup which improved the accuracy and performance of this scraper ten-fold.
# If lxml is not installing, aptitide install libxml2-dev libxslt-dev python-dev lib32z1-dev

import sys, os
import requests
from lxml import html
import urlparse
from collections import deque
import cPickle as pickle # TODO: Some sites may have maliciously crafted URLs which can break pickle, possible?
import time
from hashlib import sha512 as hash

FREEZE_FILE = "spider.pkl"
STARTING_PAGE = "http://josephcatrambone.com"
MEDIA_FOLDER = "./images/"
REVISIT_DELAY = 60*60*6 # Revisit a site no more than four times in a day

def save_state(state_vars, freeze_file=FREEZE_FILE):
	fout = open(freeze_file, 'wb')
	pickle.dump(state_vars, fout, pickle.HIGHEST_PROTOCOL)
	fout.close()

def restore_state(freeze_file=FREEZE_FILE):
	try:
		fin = open(freeze_file, 'rb')
		state = pickle.load(fin)
		fin.close()
	except IOError as ioe:
		return None
	return state

def main():
	# Set up initial state
	url_queue = deque()
	last_visit = dict()

	# Quick restore else save
	last_state = restore_state()
	if last_state:
		url_queue, visited_urls = last_state
	else:
		url_queue.append(STARTING_PAGE)
		url_queue.append("http://imgur.com")
		save_state((url_queue, last_visit))

	# Begin main search loop
	while len(url_queue):
		now = time.time()
		url = url_queue.popleft()
		if url in last_visit and now - last_visit[url] < REVISIT_DELAY:
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
			filename = image.split('/')[-1] # To avoid conflicts, hash the filename
			filename = hash(str(now) + filename).hexdigest() + filename[-4] # But keep the extension
			fout = open(os.path.join(MEDIA_FOLDER, filename), 'w') 
			fout.write(img_response.content)
			fout.close()

		# Mark this as complete and save our state
		visited_urls[url] = now
		save_state((url_queue, visited_urls))

		# Throttle
		time.sleep(1)

if __name__=="__main__":
	main()
