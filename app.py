from flask import Flask, render_template, request
import requests
import pyodbc
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Azure Face API credentialsvb
FACE_API_KEY = "F9Ml1EiGAHoMyv68NROC2pQ6Q5gGSxgVsHCgFhqoiaqcTIzK1gQqJQQJ99BFACYeBjFXJ3w3AAAKACOGGZYg"
FACE_API_ENDPOINT = "https://tioserver.cognitiveservices.azure.com/face/v1.0"

# Azure SQL Database connection
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=<your-server>.database.windows.net;DATABASE=<your-db>;UID=<user>;PWD=<password>')
cursor = conn.cursor()

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/detect', methods=['POST'])
# def detect_face():
#     image = request.files['image'].read()
#     headers = {
#         'Ocp-Apim-Subscription-Key': FACE_API_KEY,
#         'Content-Type': 'application/octet-stream'
#     }
#     params = {'returnFaceId': 'true'}
#     response = requests.post(f"{FACE_API_ENDPOINT}/detect", headers=headers, params=params, data=image)

#     if response.status_code == 200 and response.json():
#         face_id = response.json()[0]['faceId']
#         student_id = face_id  # You can map this to real student info
#         timestamp = datetime.now()

#         cursor.execute("INSERT INTO Attendance (student_id, timestamp) VALUES (?, ?)", student_id, timestamp)
#         conn.commit()
#         return "Attendance Marked"
#     else:
#         return "Face Not Detected"

@app.route('/detect', methods=['POST'])
def detect_face():
    if 'image' in request.files:
        # Handle file upload
        image = request.files['image'].read()
    elif 'webcam_image' in request.form:
        # Handle webcam base64 input
        base64_data = request.form['webcam_image'].split(',')[1]
        image = base64.b64decode(base64_data)
    else:
        return "No image provided"

    headers = {
        'Ocp-Apim-Subscription-Key': FACE_API_KEY,
        'Content-Type': 'application/octet-stream'
    }
    params = {'returnFaceId': 'true'}
    response = requests.post(f"{FACE_API_ENDPOINT}/detect", headers=headers, params=params, data=image)

    if response.status_code == 200 and response.json():
        face_id = response.json()[0]['faceId']
        timestamp = datetime.now()
        cursor.execute("INSERT INTO Attendance (student_id, timestamp) VALUES (?, ?)", face_id, timestamp)
        conn.commit()
        return "Attendance Marked"
    else:
        return "Face Not Detected"

if __name__ == '__main__':
    app.run(debug=True)
