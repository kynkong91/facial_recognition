from flask import Flask, jsonify, request, redirect
from firebase_admin import credentials, firestore, initialize_app
import requests
import os
import pyrebase
import face_recognition
import numpy as np
from google.cloud import storage
from google.oauth2 import service_account


# 1a. Initialize Firestore DB [To gain access to the DB]
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred, {
    'storageBucket': 'swifthome-swifthome-dev.appspot.com'
})

# 1b. Instantiate fire store DB
db = firestore.client()


user_encoding = db.collection('UserEncoding')

# 2a. Initialise Storage [To gain access to the storage]
config = {
    "apiKey": "AIzaSyCDu1SY5-mPnVt50JN8rlpF6BQu5szw-7o",
    "authDomain": "swiftoffice-swifthome-dev.firebaseapp.com",
    "databaseURL": "https://swiftoffice-swifthome-dev.firebaseio.com",
    "projectId": "swiftoffice-swifthome-dev",
    "storageBucket": "swiftoffice-swifthome-dev.appspot.com",
    "messagingSenderId": "954012651922",
    "serviceAccount": "key.json"
}

# 2b. Initialise pyrebase with config file
# firebase = pyrebase.initialize_app(config)

# 2c. Create a firebase storage instances


'''First attempt
photoBucket = storage.bucket('swifthome-swifthome-dev.appspot.com/Photos')
print(photoBucket.get_blob('chan_a.jpg').download_as_string())
'''


storage_client = storage.Client.from_service_account_json(
    'service_account.json')

thebucket = storage_client.get_bucket('swiftoffice-swifthome-dev.appspot.com')

the_list = ["chan_a.jpg", "chan_b.jpg"]

for url in the_list:
    img_blob = thebucket.get_blob('Photos/' + url)
    print(img_blob)
    img_blob.download_to_filename('temp_img/' + url)

'''
with open("temp_img/chan_a.jpg", "wb") as file_obj:
    img_blob.download_to_file(file_obj)
print(img_blob)

# Make an authenticated API request
# buckets = list(storage_client.list_buckets())
# print(bucket)
'''
