#!/usr/bin/env python
# spider.py -- The job which browses pages in the background, pulls images, and pushes them into the database.
# Credit to Jake Austwick for an awesome scraper writeup which improved the accuracy and performance of this scraper ten-fold.
# If lxml is not installing, aptitide install libxml2-dev libxslt-dev python-dev lib32z1-dev

import sys, os
import logging
import fnmatch # For glob matching in robots.txt
from StringIO import StringIO
from PIL import Image
import requests
from lxml import html
import urlparse
from collections import deque
import cPickle as pickle # TODO: Some sites may have maliciously crafted URLs which can break pickle, possible?
import time
from hashlib import sha512 as hash

from settings import MEDIA_ROOT, MIN_IMAGE_SIZE

BOT_NAME = "ImageSearch_Bot"
FREEZE_FILE = "spider.pkl"
STARTING_PAGE = "http://josephcatrambone.com/spider.html"
REVISIT_DELAY = 60*60*6 # Revisit a site no more than four times in a day
HEADERS = {'User-Agent': BOT_NAME, 'From': "jo.jcat@gmail.com"}

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

def spider_allowed(url, robot_rules):
	# Get the domain of the URL
	# http://www.josephcatrambone.com/robots.txt -> josephcatrambone.com
	url = url.lower()

	# From Wikipedia: The rules for http and https apply separately, and robots only applies to a single origin.
	# That means http://a.example.com needs a robots.txt and http://example.com needs a different robots.txt.
	# Thus, we can ignore this next part that strips off the https://blah.foo.etc.example.com
	#if url.startswith("https://"):
	#	url = url[len("https://"):]
	#if url.startswith("http://"):
	#	url = url[len("http://"):]
	url = url[:url.find("/", len("https://")+1)]

	if url not in robot_rules:
		try:
			rules = list()

			response = requests.get(url + "/robots.txt")
			if response.ok:	
				# Split the rules into one rule per line and remove the comments.
				comment_stripped = [rule[:rule.find("#")] for rule in response.content.split("\n")]
				empty_stripped = [rule for rule in comment_stripped if len(rule) > 0]
				# For each line, read either the diallowed or the user-agent command.
				# If the user-agent command is found, check if it applies to us or ALL bots.
				# If it's the disallowed command, append the disallowed sites to our rules list.
				applies_to_our_spider = False
				for line in empty_stripped:
					chunks = line.split(":")
					command = chunks[0].lower()
					target = chunks[1].strip()
					if command == "user-agent":
						if target == BOT_NAME or target == "*":
							applies_to_our_spider = True
						else:
							applies_to_our_spider = False
					elif command == "disallow":
						if not applies_to_our_spider:
							continue
						rules.append(target)

			robot_rules[url] = rules

		except IOError as ioe:
			return True
		except requests.exceptions.ConnectionError as ce:
			return True

	# We could perhaps translate the fnmatch pattern to regex with trnslate, but fnmatch looks better.
	# If a rule fnmatches our url, then the robots.txt file has disallowed our reading of that file.
	for rule in robot_rules[url]:
		if fnmatch.fnmatch(url, rule):
			return False

	return True # It is allowed.

	

def main():
	# Set up initial state
	url_queue = deque()
	last_visit = dict()
	robot_rules = dict()

	# Quick restore else save
	last_state = restore_state()
	if last_state:
		robot_rules, url_queue, last_visit = last_state
	else:
		url_queue.append(STARTING_PAGE)
		save_state((robot_rules, url_queue, last_visit))

	# Begin main search loop
	while len(url_queue):
		now = time.time()
		url = url_queue.popleft()

		# If it is too early to revisit, skip this URL
		if url in last_visit and now - last_visit[url] < REVISIT_DELAY:
			continue

		# If the robots.txt file of this domain does not allow us, skip
		if not spider_allowed(url, robot_rules):
			logging.info("spider.py: main: robots.txt not allowing {}".format(url))
			continue

		# Dump to logs
		logging.info("spider.py: main: Visiting page {}".format(url))

		# Get the page
		response = None
		parsed_body = None
		try:
			response = requests.get(url, headers=HEADERS)
			parsed_body = html.fromstring(response.content)
		except requests.exceptions.ConnectionError as ce:
			logging.info("spider.py: main: Connection error while getting url {}".format(url))
			continue
		except lxml.etree.XMLSyntaxError as xse:
			logging.info("spider.py: main: Couldn't parse XML/HTML for url {}".format(url))
			continue

		# Find URLs
		outbound_urls = [urlparse.urljoin(response.url, url) for url in parsed_body.xpath('//a/@href')]
		image_urls = [urlparse.urljoin(response.url, url) for url in parsed_body.xpath('//img/@src')]

		# Handle the URLs
		for new_url in outbound_urls:
			if new_url.startswith('http'):
				url_queue.append(new_url)
		for image in image_urls:
			# Check to see if we did a get for this URL within the last time span
			if image in last_visit and now - last_visit[image] < REVISIT_DELAY:
				continue;
			try:
				# Otherwise get the image
				img_response = requests.get(image)
				# Mark our read time
				last_visit[image] = now
				# Read as image
				temp_io = StringIO(img_response.content)
				temp_io.seek(0)
				img = Image.open(temp_io)
				if img.size[0] < MIN_IMAGE_SIZE or img.size[1] < MIN_IMAGE_SIZE:
					continue
				# Save to file
				filename = image.split('/')[-1] # To avoid conflicts, hash the filename
				#filename = hash(str(now) + filename).hexdigest() + filename[-4:] # But keep the extension
				filename = hash(img.tostring()).hexdigest() + filename[-4:]
				filepath = os.path.join(MEDIA_ROOT, filename)
				if not os.path.isfile(filepath):
					fout = open(filepath, 'w') 
					fout.write(img_response.content)
					fout.close()
				else:
					logging.info("spider.py: main: Image already saved {}".format(image))
				# Push to database
				pass
				# Push to log
				logging.info("spider.py: main: Added image {} -> {}".format(image, filename[:10] + ".." + filename[-10:]))
			except IOError as ioe:
				logging.warn("spider.py: main: IOException while processing url {}: {}".format(image, str(ioe)))
			except requests.packages.urllib3.exceptions.LocationParseError as pe:
				logging.warn("spider.py: main: LocationParseError while getting url {}".format(image))

		# Mark this as complete and save our state
		last_visit[url] = now
		save_state((robot_rules, url_queue, last_visit))

		# Throttle
		time.sleep(1)

if __name__=="__main__":
	main()
