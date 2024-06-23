import cv2
from keras.models import model_from_json
import numpy as np
import time

# Load the pre-trained model
json_file = open("facialemotionmodel.json", "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights("facialemotionmodel.h5")

# Load Haar Cascade classifier for face detection
haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)

def extract_features(image):
    # Convert image to numpy array and reshape
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0

# Initialize webcam
webcam = cv2.VideoCapture(0)

# Emotion labels dictionary
labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

# Initialize variables to store recent emotions
recent_emotions = []
num_recent_frames = 3  # Number of frames to consider

# Start timer
start_time = time.time()
duration = 5  # Duration to run the emotion detection in seconds

while True:
    ret, im = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(im, 1.3, 5)
    
    try:
        for (p, q, r, s) in faces:
            image = gray[q:q + s, p:p + r]
            cv2.rectangle(im, (p, q), (p + r, q + s), (255, 0, 0), 2)
            image = cv2.resize(image, (48, 48))
            img = extract_features(image)
            pred = model.predict(img)
            prediction_label = np.argmax(pred)
            recent_emotions.append(prediction_label)
            
            # Display emotion label and accuracy
            accuracy = pred.max() * 100
            cv2.putText(im, f'{labels[prediction_label]} ({accuracy:.2f}%)', (p - 10, q - 10),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255))
        
        # Keep only the last few emotions
        if len(recent_emotions) > num_recent_frames:
            recent_emotions.pop(0)
        
        # Display recent emotions
        cv2.putText(im, 'Recent Emotions:', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        for i, emotion in enumerate(recent_emotions):
            cv2.putText(im, f'{i+1}. {labels[emotion]}', (10, 60 + i*30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        cv2.imshow("Output", im)
        
        # Check if the elapsed time is greater than the duration
        if time.time() - start_time > duration:
            # Save the last frame as an image
            cv2.imwrite("last_frame.jpg", im)
            
            # Save the most predicted emotion to a file
            most_predicted_emotion = max(set(recent_emotions), key=recent_emotions.count)
            with open("predicted_emotion.txt", "w") as file:
                file.write(labels[most_predicted_emotion])
            
            break
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    except cv2.error:
        pass

# Release the webcam
webcam.release()
cv2.destroyAllWindows()
