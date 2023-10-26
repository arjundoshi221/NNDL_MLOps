import cv2
import numpy as np
from keras.models import model_from_json


pedestrian_dict = {0: "None", 1: "Pedestrian"}

ask = input("Which model do you wanna use?")

if ask == "vgg":
    
# load json and create model
    json_file = open('VGG19/VGG19_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    pedestrian_model = model_from_json(loaded_model_json)

# load weights into new model
    pedestrian_model.load_weights("VGG19\VGG19_model.h5")
    print("Loaded model from disk")

if ask == "resnet":
    
# load json and create model
    json_file = open('Resnet101/ResNet101_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    pedestrian_model = model_from_json(loaded_model_json)

# load weights into new model
    pedestrian_model.load_weights("Resnet101\ResNet101_model.h5")
    print("Loaded model from disk")

if ask == "inception":
    
# load json and create model
    json_file = open('Inceptionv3/inceptionv3_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    pedestrian_model = model_from_json(loaded_model_json)

# load weights into new model
    pedestrian_model.load_weights("Inceptionv3\inceptionv3_model.h5")
    print("Loaded model from disk")
# start the webcam feed
#cap = cv2.VideoCapture(0)

# pass here your video path
# you may download one from here : https://www.pexels.com/video/three-girls-laughing-5273028/


cap = cv2.VideoCapture("testvid2.mp4")

while True:
    # Find haar cascade to draw bounding box around face
    ret, frame = cap.read()
    if not ret:
        # End of the video, break out of the loop
        break
    frame = cv2.resize(frame, (1280, 720))
    if not ret:
        break
    pedestrian_detector = cv2.CascadeClassifier('haarcascade/haarcascade_fullbody.xml')
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # detect faces available on camera
    num_peds = pedestrian_detector.detectMultiScale(rgb_frame, scaleFactor=1.3, minNeighbors=5)
    print(f"Number of pedestrians detected: {len(num_peds)}")

    # take each face available on the camera and Preprocess it
    for (x, y, w, h) in num_peds:
        cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
        roi_rgb_frame = rgb_frame[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_rgb_frame, (200, 200)), -1), 0)

        # predict the emotions
        emotion_prediction = pedestrian_model.predict(cropped_img)
        maxindex = int(np.argmax(emotion_prediction))
        cv2.putText(frame, pedestrian_dict[maxindex], (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        
    cv2.imshow('Pedestrian Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
