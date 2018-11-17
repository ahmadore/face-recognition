from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators import csrf
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import numpy as np

from .models import Report
from .serializers import ReportSerializer

# path to encoding file
encodings_path = "../encodings.pickle"

# load encoding into memory
data = pickle.loads(open(encodings_path, "rb").read())

encodings = data["encodings"]
names = data["names"]

def encode_image(image):
    img_raw = image.read()
    np_img = np.fromstring(img_raw, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # detect the coordinates of the bounding box of each face in the image
    boxes = face_recognition.face_locations(rgb, model='cnn')
    # compute the facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, boxes)
    return encodings

def serialize_data(data):
    with open(encodings_path, "wb") as f:
        f.write(pickle.dumps(data))
    return None

# Create your views here.
def index(request):
    return render(request, "index.html")

def report(request):
    return render(request, "report.html")

def find(request):
    return render(request, "find.html")

@csrf.csrf_exempt
def report_api(request):
    if request.method == "POST":
        form = request.POST
        first_name = form["first_name"]
        last_name = form["last_name"]
        other_name = form["other_name"]
        phone_number = form["phone_number"]
        address = form["address"]
        images = request.FILES.getlist('images')
        report = Report(
            first_name=first_name, last_name=last_name, other_name=other_name, 
            address=address, phone_number=phone_number, photo=images[0]
        )
        report.save()
        # encode images
        for image in images[1:]:
            encoded = encode_image(image)
            for code in encoded:
                encodings.append(code)
                names.append(report.id)
        data = {
            "encodings": encodings,
            "names": names
        }
        serialize_data(data)
        return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'status': 'failed'}), content_type="application/json")

@csrf.csrf_exempt
def find_api(request):
    image = request.FILES["image"]
    encodings = encode_image(image)
    names = []
    # attempt to match each detected face to know images
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"
        if True in matches:
            # find the index of all matched faces and count their occurance
            matched_idx = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            
            # loop over matched indexes and maintain a count of each face
            for i in matched_idx:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            
            # determine the name with the maximum vote
            name = max(counts, key=counts.get)
        
        # update lists of names
        names.append(name)
    try:
        found = Report.objects.filter(pk__in=names)
        sFound = ReportSerializer(found, many=True).data
        response = {
            'found': 'true',
            'data' : sFound[0]
        }
        return HttpResponse(json.dumps(response), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'found': 'false'}), content_type="application/json")