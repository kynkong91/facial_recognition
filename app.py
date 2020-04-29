# NOTE: This example requires flask to be installed! You can install it with pip:
# $ pip3 install flask

# Test case: Encode pictures
# curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"image_urls":["chan_a.jpg","chan_b.jpg"]}' http://0.0.0.0:5000/encode_and_upload
# curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"image_urls":["jet_li.jpg"]}' http://0.0.0.0:5000/encode_and_upload


# Test case: Facial Recognition
# curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"image_urls":["chan_a.jpg","chan_b.jpg","jet_li.jpg","positive2.jpg"]}' http://0.0.0.0:5000/facial_recognition


from flask import Flask, jsonify, request, redirect
#from firebase_admin import credentials, firestore, initialize_app
import requests
import os
#import pyrebase
#import face_recognition
import numpy as np

'''
# 1a. Initialize Firestore DB [To gain access to the DB]
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred, {
    'storageBucket': 'swifthome-swifthome-dev.appspot.com'
})

# 1b. Instantiate fire store DB
db = firestore.client()

# 1c. Handle to store/retrieve user image encoding
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
firebase = pyrebase.initialize_app(config)

# 2c. Create a firebase storage instances
storage = firebase.storage()
'''

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


'''
# Perform encoding and return a dict of {'filename':encoding} [Tested and passed]
@app.route('/encode_and_upload', methods=['POST'])
def perform_encoding_and_upload():

    # Grab the urls from requests
    image_urls = request.get_json()['image_urls']

    if len(image_urls) > 0:
        for image_url in image_urls:

            # Temporarily download image
            tempfile_url = download_image(image_url)

            # Perform face encoding
            face_encoding = encode_image(tempfile_url)
            face_encoding_json = {image_url: face_encoding.tolist()}

            # Delete the images in the temp storage
            delete_image(tempfile_url)

            try:
                # Store the face encoding in the firebase
                user_encoding.document(image_url).set(face_encoding_json)

            except Exception as e:
                return f"An Error Occured: {e}"

        return jsonify({"success": True}), 200

    else:

        return jsonify({"error": "You did not include any photo links in your request"}), 200


# Image recognition by comparing encoding and return a dict of {'status':true}
@app.route('/facial_recognition', methods=['POST'])
def facial_recognition():

    # extract image urls
    image_urls = request.get_json()['image_urls']

    if len(image_urls) > 0:

        # Create list to store kwown face encoding
        known_face_encoding_arr = []

        # Grab encoding of known face from firebase
        for image_url in image_urls[1:]:
            known_face_encoding = user_encoding.document(image_url).get()
            known_face_encoding_formatted = known_face_encoding.to_dict()[
                image_url]
            known_face_encoding_arr.append(known_face_encoding_formatted)

        # Temporarily download image
        unknown_face_url = image_urls[0]
        tempfile_url = download_image(unknown_face_url)

        # Perform face encoding
        unknown_face_encoding = encode_image(tempfile_url)

        # Delete the image in the temp storage (for unknown face)
        delete_image(tempfile_url)

        # image facial features
        match_results = image_comparison(
            known_face_encoding_arr, unknown_face_encoding)

        return {'result': str(match_results)}, 200

    else:

        return jsonify({"error": "You did not include any photo links in your request"}), 200


############################
###Auxilary Methods below###
############################

# Grab image and download into temp folder
def download_image(image_url):
     # the url to download image from
    download_url = "Photos/" + image_url

    # the url to upload image to
    tempfile_url = "temp_img/" + image_url

    # download image to temporary storage
    storage.child(download_url).download(tempfile_url)

    return tempfile_url

# Delete image from temp folder


def delete_image(image_url):

    # Delete the images in the temp storage
    if os.path.exists(image_url):
        os.remove(image_url)
    else:
        print("The file does not exist")


# Perform Image encoding
def encode_image(img_url):
    the_image = face_recognition.load_image_file(img_url)
    face_encoding = face_recognition.face_encodings(
        the_image, num_jitters=100)[0]

    return face_encoding


# Perform Image comparison
def image_comparison(known_face_encoding_arr, unknown_face_encoding):
    match_results = face_recognition.compare_faces(
        known_face_encoding_arr, unknown_face_encoding, tolerance=0.39)

    # This count the number of matches
    return sum(match_results) > 1
'''

if __name__ == '__main__':
    app.run()
