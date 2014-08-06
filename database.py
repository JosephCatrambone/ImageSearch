#!/usr/bin/env python
# database.py -- The shared access functions which deal with the database

import sys, os
import psycopg2, psycopg2.extras
from datetime import datetime, timedelta
import atexit

# Obtain a database connection and close on quit to avoid leaking
db = psycopg2.connect(host=os.environ['DB_HOST'], dbname=os.environ['DB_NAME'], user=os.environ['DB_USER'], password=os.environ['DB_PASSWORD'])
def close_database():
	db.close()
atexit.register(close_database)

# Database schema creation
def make_database_schema():
	cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("""CREATE FUNCTION HAMMING_DISTANCE(bytea, bytea) RETURNS integer AS 'hamming.so', 'HAMMING_DISTANCE' LANGUAGE C STRICT;""") # Requires building the hamming func.
	cursor.execute("""CREATE SEQUENCE images_id_seq""")
	cursor.execute("""CREATE SEQUENCE hashes_id_seq""")
	cursor.execute("""CREATE TABLE images (id INTEGER NOT NULL DEFAULT nextval('images_id_seq') PRIMARY KEY, url TEXT, parent_url TEXT, filename TEXT, modified TIMESTAMP DEFAULT now())""") # Max URL among web browsers: 2083
	cursor.execute("""CREATE TABLE hashes (id INTEGER NOT NULL DEFAULT nextval('hashes_id_seq') PRIMARY KEY, image_id INTEGER REFERENCES images (id), data BYTEA, algorithm TEXT, modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
	db.commit()
	cursor.close()

# Begin shared API functions
def create_image(url, parent_url, image_filename):
	cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("INSERT INTO image (url, parent_url, filename) VALUES (%s, %s, %s)", (url, parent_url, image_filename))
	db.commit()
	cursor.close()

def find_images(hash, algorithm, result_limit=50, result_offset=0):
	cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("""
	SELECT 
		images.id, images.url, images.parent_url, images.filename, HAMMING_DISTANCE(%s, hashes.data) as distance 
	FROM 
		images, hashes 
	WHERE 
		hashes.algorithm=%s AND images.id = hashes.image_id 
	ORDER BY 
		distance 
	LIMIT %s
	OFFSET %s""",
	(psycopg2.Binary(hash), algorithm, result_limit, result_offset))
	result = cursor.fetchall()
	cursor.close()
	return result

def find_images_without_hash(algorithm):
	cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT images.id, images.filename FROM images WHERE NOT EXISTS (SELECT 1 FROM hashes WHERE images.id=hashes.image_id)")
	# SELECT images.id, images.filename FROM images LEFT JOIN hashes ON images.id=hashes.image_id WHERE hashes.image_id is NULL;
	result = cursor.fetchall()
	cursor.close()
	return result

def create_hash(image_id, hash_value, hash_algorithm):
	cursor = db.cursor()
	psycopg2.Binary(h)
	cursor.execute("INSERT INTO hashes (image_id, data, algorithm) VALUES (%s, %s, %s)", (image_id, psycopg2.Binary(hash_value), hash_algorithm))
	db.commit()
	cursor.close()

def clean_old_images(timeago, valid_entry, update_last_access=True):
	"""Selects images older than timeago and, for each image, runs valid_entry(image). If valid_entry returns false, removes the image."""
	now = datetime.now()
	updated = 0
	deleted = 0
	cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute('SELECT * FROM images WHERE modified < %s', ((now-timedelta(seconds=timeago)), ))
	results = cursor.fetchall();
	for row in results: # Can't do for row in cursor since we're updating it.
		if valid_entry(row):
			cursor.execute("UPDATE images SET modified=%s WHERE id=%s", (now, row['id']))
			updated += 1
		else:
			cursor.execute("DELETE FROM images WHERE id=%s", (row['id'], ))
			deleted += 1
	db.commit()
	cursor.close()
	return updated, deleted

def clean_old_hashes():
	"""Remove hashes whose parent image has been deleted.  May not be necessary if REMOVE WITH CASCADE is done."""
	pass
