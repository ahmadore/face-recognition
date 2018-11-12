from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

# Construct argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True, 
    help="directory of training dataset")
ap.add_argument("-e", "--encodings", required=True, 
    help="path to save serialized db of encoded faces")
ap.add_argument("-d", "--detection_method", default="cnn",
    help="face detection model to use: options are 'hog' and 'cnn'")

args = vars(ap.parse_args())

#  get the path to our training dataset
print("[INFO] quantifying faces...")
image_paths = list(paths.list_images(args["dataset"]))

# initialize list of known encodings and names

known_encodings = []
known_names = []

# loop through image paths
for i, image_path in enumerate(image_paths):
    # extract the person's name form the image path
    print("[INFO] processing image {}/{}".format(i +1, len(image_paths)))
    name = image_path.split(os.path.sep)[-2]

    # load the input image and convrt it from BGR (openCV format)
    # to dlib's RGB format
    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect the coordinates of the bounding box of each face in the image
    boxes = face_recognition.face_locations(rgb, model=args["detection_method"])
    
    # compute the facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, boxes)

    #  add all encodings and names to list of know encodings and names
    for encoding in encodings:
        known_encodings.append(encoding)
        known_names.append(name)

# dump dataset to disc
print(["INFO] serializing encodings..."])
data = {
    "encodings": known_encodings,
    "names": known_names
}

with open(args["encodings"], "wb") as f:
    f.write(pickle.dumps(data))
