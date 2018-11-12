import face_recognition
import argparse
import pickle
import cv2

# construct the argument parser to parse the argument
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True, 
    help="path to serialized db of facial encoding")
ap.add_argument("-i", "--image", required=True, 
    help="path to input image")
ap.add_argument("-d", "--detection-method", default="cnn", 
    help="face detection model to use: either 'hog' or 'cnn'")

args = vars(ap.parse_args())

print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())

# load the input image and convert it to RBG from BGR
print(args["image"])
image = cv2.imread(args["image"])
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# detect (x, y) - coordinates of bounding boxes coresponding to each face in
# the input image, then compute the facial embeddings for each face
print("[INFO] recognizing faces...")
boxes = face_recognition.face_locations(rgb, model=args["detection_method"])
encodings = face_recognition.face_encodings(rgb, boxes)

# initialize the list of names for each face detected

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

# visualize the resut
for ((top, right, bottom, left), name) in zip(boxes, names):
    # draw the pricted face name on the image
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    y = top - 15 if top - 15 > 15 else top + 15
    cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
        0.75, (0, 255, 0), 2)

# show image
cv2.imshow("Image", image)
cv2.waitKey(0)


