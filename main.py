import config

import cv2
import dlib

from image_preprocessor import ImagePreprocessor
from emotion_predictor import  EmotionPredictor
from client import Client
from rect import Rect

from emotions import emotion_label

IS_NEED_TO_SEND_MESSAGE = config.IS_NEED_TO_SEND_MESSAGE
HOST = config.HOST
PORT = config.PORT
SHAPE_PREDICT_MODEL = config.SHAPE_PREDICT_MODEL

def PredictEmotion(frame, face_rects, scores):
    # Pick biggest face
    biggest_length = 0
    nearest_face = 0
    for idx, face_rect in enumerate(face_rects):
        length = face_rect.right() - face_rect.left()
        print(length)
        if length > biggest_length:
            biggest_length = length
            nearest_face = idx
            
    # Mark face & score
    face_rect = face_rects[nearest_face]
    head_rect = Rect(face_rect.top(), face_rect.bottom(), face_rect.left(), face_rect.right())
    head_rect.FitFaceToHeadSize()
    x1 = head_rect.Left
    y1 = head_rect.Top
    x2 = head_rect.Right
    y2 = head_rect.Bottom
    text = "%2.2f" % (scores[nearest_face])

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
    cv2.putText(frame, text, (x1, y1), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

    # Preprocessing image
    preprocessor = ImagePreprocessor()
    try:
        transform_image = preprocessor.Transform(frame, head_rect)

        # Predict emotion
        emotion_predictor = EmotionPredictor()
        score, emotion = emotion_predictor.Predict(transform_image)
        cv2.putText(frame, emotion_label[emotion], (0, 100), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 1)

        if IS_NEED_TO_SEND_MESSAGE:
            message = '&Score = ' + str(score) + ', &Emotion = ' + str(emotion) + '\n'
            client.Send(message)
    except:
        print('Exception')

camera = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor(SHAPE_PREDICT_MODEL)

if not camera.isOpened():
    print('Cannot open camera')
    exit()

client = Client(HOST, PORT)
if IS_NEED_TO_SEND_MESSAGE:
    client.Connect()

while True:
    # Regist to server
    if IS_NEED_TO_SEND_MESSAGE:
        if '%NAME' in client.Receive():
            client.Send('&NAME|FER\n')
    
    # ret : Is read image?
    ret, frame = camera.read()

    if (not ret) or (len(frame) <= 0):
        print('Cannot receive frame')
        continue

    # Detect face
    face_rects, scores, idx = detector.run(frame, 0)

    if len(face_rects) != 0:
        PredictEmotion(frame, face_rects, scores)

    # Show frame
    cv2.imshow('camera2', frame)

    # Press q to exit
    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
