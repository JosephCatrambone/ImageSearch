from __future__ import division
import sys, os
import sqlite3
import atexit
import base64
import json
from hashlib import sha512 as hash
from StringIO import StringIO
from glob import glob
from random import randint, choice
from PIL import Image
from flask import Flask, request, g, render_template, Response
from datetime import datetime, timedelta

import settings
import database

# Globals
app = Flask(__name__);
app.secret_key = settings.SHARED_SECRET;
STATIC_FILES = os.environ.get('STATIC_FILE_PATH', "static");

# Routes
@app.route("/")
@app.route("/index.html")
def index():
	return app.send_static_file(os.path.join(STATIC_FILES, 'index.html'));
	#return render_template('index.html');

@app.route("/static/<path:path>")
def serve_static(path):
	return app.send_static_file(os.path.join(STATIC_FILES, path));
	#return send_from_directory(os.path.join(STATIC_FILES, path));

@app.route("/img/<int:id>")
def get_image(id):
	result = database.get_image(id);
	return  

# Ajax calls by the end users.
@app.route("/search")
@app.route("/search/<algorithm>")
def run_search(algorithm=None):
	return Response("Response!");

@app.route("/get_work") #, methods=['GET'])
def get_work():
	return Response(json.dumps(content), mimetype="application/json");

# Helper functions
def decode_img_from_base64(imgdata):
	fio = StringIO();
	fio.write(base64.b64decode(imgdata));
	img = Image.open(fio.getvalue());
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
