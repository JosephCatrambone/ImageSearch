#!/usr/bin/env python
# database.py -- The shared image creation and hashing functions which deal with the database

import sys, os
import psycopg2, psycopg2.extras
import time
import atexit

# Obtain a database connection and close on quit to avoid leaking
connection = psycopg2.connect("host='{}' dbname='{}' user='{}' password='{}'".format(os.environ['DB_HOST'], os.environ['DB_NAME'], os.environ['DB_USER'], os.environ['DB_PASSWORD']))
def close_database():
	connection.close()
atexit.register(close_database)

# Begin shared API functions
def create_image(url, parent_url, image_filename):
	pass

def get_images_before(timeago, update_last_access=True):
	now = time.time()
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute('SELECT * FROM images WHERE lastmodified < %s', (int(now-timeago), ))
	records = cursor.fetchall()
	cursor.execute('UPDATE image SET lastmodified = %s WHERE lastmodified < %s', (int(now), int(now-timeago)))
		


