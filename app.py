import face_recognition
from flask import Flask, jsonify, request, redirect
from firebase_admin import credentials, firestore, initialize_app
import requests
import os
import pyrebase
import face_recognition
import numpy as np


app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()
