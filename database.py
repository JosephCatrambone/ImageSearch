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
def create_database_schema():
	cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	#cursor.execute("""CREATE FUNCTION HAMMING_DISTANCE(bytea, bytea) RETURNS integer AS 'hamming.so', 'HAMMING_DISTANCE' LANGUAGE C STRICT;""") # Requires building the hamming func.
	cursor.execute("""CREATE SEQUENCE images_id_seq""")
	cursor.execute("""CREATE SEQUENCE pages_id_seq""")
	cursor.execute("""CREATE SEQUENCE hashes_id_seq""")
	cursor.execute("""CREATE TABLE images (id INTEGER NOT NULL DEFAULT nextval('images_id_seq') PRIMARY KEY, url TEXT, filename TEXT, modified TIMESTAMP DEFAULT now())""") # Max URL among web browsers: 2083
	cursor.execute("""CREATE TABLE pages (id INTEGER NOT NULL DEFAULT nextval('pages_id_seq') PRIMARY KEY, image_id INTEGER REFERENCES images(id), url TEXT, modified TIMESTAMP DEFAULT now())""")
	cursor.execute("""CREATE TABLE hashes (id INTEGER NOT NULL DEFAULT nextval('hashes_id_seq') PRIMARY KEY, image_id INTEGER REFERENCES images (id), data BYTEA, algorithm TEXT, modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
	db.commit()
	cursor.close()

def destroy_database_schema():
	if raw_input("Are you sure? [yes/no]: ") == "yes":
		cursor = db.cursor()
		cursor.execute("DROP TABLE hashes")
		cursor.execute("DROP TABLE pages")
		cursor.execute("DROP TABLE images")
		cursor.execute("DROP SEQUENCE images_id_seq")
		cursor.execute("DROP SEQUENCE pages_id_seq")
		cursor.execute("DROP SEQUENCE hashes_id_seq")
		db.commit()
		cursor.close()
	else:
		print("Did not get yes.  Aborting.")

# Begin shared API functions
def create_image(url, parent_url, image_filename):
	cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("INSERT INTO image (url, parent_url, filename) VALUES (%s, %s, %s) RETURNING id", (url, parent_url, image_filename))
	new_id = cursor.fetchone()[0]
	db.commit()
	cursor.close()
	return new_id

def create_page(url, image_filename=None, image_id=None):
	cursor = db.cursor()

	if image_id is None:
		if image_filename is None:
			cursor.close()
			raise ValueError("Error while creating page for url {}.  Image filename and id are none.".format(url))
		else: # Look up image_id from image_filename
			cursor.execute("SELECT id FROM images WHERE filename=%s LIMIT 1", (image_filename,))
			image_id = cursor.fetchone()[0]

	cursor.execute("INSERT INTO pages (image_id, url) VALUES (%s, %s) RETURNING id", (image_id, url))
	new_id = cursor.fetchone()[0]

	db.commit()
	cursor.close()
	return new_id

def create_hash(image_id, hash_value, hash_algorithm):
	cursor = db.cursor()
	psycopg2.Binary(h)
	cursor.execute("INSERT INTO hashes (image_id, data, algorithm) VALUES (%s, %s, %s) RETURNING id", (image_id, psycopg2.Binary(hash_value), hash_algorithm))
	new_id = cursor.fetchone()[0]
	db.commit()
	cursor.close()
	return new_id

def get_image(id):
	cursor = db.cursor()
	cursor.execute("SELECT * FROM images WHERE id=%s", (id,))
	result = cursor.fetchone()
	cursor.close()
	return result

def get_images_from_ids(ids):
	cursor = db.cursor()
	cursor.execute("SELECT * FROM images WHERE id IN %s", (ids,))
	result = cursor.fetchall()
	cursor.close()
	return result

def get_images_from_hash(hash, algorithm, result_limit=50, result_offset=0):
	cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("""
	SELECT 
		images.id, images.url, images.filename, HAMMING_DISTANCE(%s, hashes.data) as distance 
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

def get_page(image_id):
	cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM pages WHERE image_id=%s", (image_id,))
	result = cursor.fetchone()
	cursor.close()
	return result

def get_pages(image_ids, result_limit=50, result_offset=0):
	raise NotImplemented() # Not done
	cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("""
	SELECT
		*
	FROM
		pages
	WHERE
		image_id IN %s
	ORDER BY
		distance
	LIMIT %s
	OFFSET %s
	""",
	(image_ids, result_limit, result_offset))
	result = cursor.fetchall()
	cursor.close()
	return result

def get_images_without_hash(algorithm):
	cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT images.id, images.filename FROM images WHERE NOT EXISTS (SELECT 1 FROM hashes WHERE images.id=hashes.image_id)")
	# SELECT images.id, images.filename FROM images LEFT JOIN hashes ON images.id=hashes.image_id WHERE hashes.image_id is NULL;
	result = cursor.fetchall()
	cursor.close()
	return result

def get_old_images(timeago, update_last_access=True):
	"""Selects images older than timeago."""
	now = datetime.now()
	updated = 0
	deleted = 0
	cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute('SELECT * FROM images WHERE modified < %s', ((now-timedelta(seconds=timeago)), ))
	results = cursor.fetchall();
	cursor.execute('UPDATE images SET modified = %s WHERE modified < %s', (now, (now-timedelta(seconds=timeago))))
	db.commit()
	cursor.close()
	return results 

def delete_images(image_ids):
	"""Drop image IDs and related pages/hashes."""
	cursor = db.cursor()
	cursor.execute('DELETE FROM hashes WHERE hashes.image_id IN %s', (image_ids, ))
	cursor.execute('DELETE FROM pages WHERE pages.image_id IN %s', (image_ids, ))
	cursor.execute('DELETE FROM images WHERE id IN %s', (image_ids, ))
	db.commit()
	cursor.close()
	return None

