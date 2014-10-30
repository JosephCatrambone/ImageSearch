from __future__ import division
import sys, os
import sqlite3
import atexit
import base64
import json
from hashlib import sha512 as hash
from cStringIO import StringIO
from glob import glob
from random import randint, choice
from PIL import Image
from flask import Flask, request, g, render_template, Response, send_from_directory
from werkzeug.contrib.fixers import ProxyFix
from datetime import datetime, timedelta

import settings
import database
import hashtools

# Globals
app = Flask(__name__);
app.secret_key = settings.SHARED_SECRET;
app.wsgi_app = ProxyFix(app.wsgi_app) # For Gunicorn.
STATIC_FILES = os.environ.get('STATIC_FILE_PATH', "static");

# Ajax calls by the end users.
@app.route("/search", methods=['POST'])
@app.route("/search/<algorithm>", methods=['POST'])
def run_search(algorithm=None):
	response = {'success':False, 'results':[]};
	imageData = request.form['imageData']; # TODO: Add error checking.
	algorithm = request.form['algorithm'];

	if algorithm is None or algorithm == "" or algorithm == "default":
		algorithm = "exact"; # Our default for now.

	if algorithm in hashtools.HASH_ALGORITHMS.keys():
		image = decode_img_from_base64(imageData);
		hash = hashtools.HASH_ALGORITHMS[algorithm](image);
		result_set = database.get_images_from_hash(hash, algorithm);
		response['results'] = result_set;
		response['success'] = True;
	return Response(json.dumps(response), mimetype="application/json");

# Web frontend data
@app.route("/img/id/<int:id>")
def get_image_by_id(id):
	result = database.get_image(id);
	return result[1:];

@app.route("/images/<filename>")
def get_image(filename):
	return send_from_directory(settings.MEDIA_ROOT, filename, as_attachment=False);

@app.route("/", methods=['GET'])
@app.route("/<path:path>", methods=['GET'])
def serve_static(path="index.html"):
	return app.send_static_file(path);
	#return send_from_directory(os.path.join(STATIC_FILES, path));

# Helper functions
def decode_img_from_base64(imgdata):
	fio = StringIO(base64.b64decode(imgdata));
	img = Image.open(fio);
	img.load();
	fio.close();
	return img;

def encode_img_as_base64_png(img):
	sout = StringIO();
	img.save(sout, format='PNG');
	contents = sout.getvalue();
	sout.close();
	return base64.b64encode(contents);

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=4567);
