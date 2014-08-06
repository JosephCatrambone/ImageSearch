from __future__ import division
import sys, os
import sqlite3
import atexit
import base64
import json
from StringIO import StringIO
from glob import glob
from random import randint, choice
from PIL import Image
from flask import Flask, request, g, render_template, Response

# Globals
app = Flask(__name__);
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

# Ajax Calls
@app.route("/get_work") #, methods=['GET'])
def get_work():
        return Response(json.dumps(content), mimetype="application/json");

# Helper functions
def encode_img_as_base64_png(img):
        sout = StringIO();
        img.save(sout, format='PNG');
        contents = sout.getvalue();
        sout.close();
        return base64.b64encode(contents);

if __name__ == "__main__":
        app.run(debug=True, host='0.0.0.0', port=5000);
