import cv2
import dlib

from image_preprocessor import ImagePreprocessor
from emotion_predictor import  EmotionPredictor
from client import Client

from emotions import emotion_label

IS_NEED_TO_SEND_MESSAGE = True
HOST = '10.120.10.201'
PORT = 6321

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
    rect = face_rects[nearest_face]
    x1 = rect.left()
    y1 = rect.top()
    x2 = rect.right()
    y2 = rect.bottom()
    text = "%2.2f" % (scores[nearest_face])

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
    cv2.putText(frame, text, (x1, y1), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

    # Preprocessing image
    preprocessor = ImagePreprocessor()
    try:
        transform_image = preprocessor.Transform(frame, rect)

        # Predict emotion
        emotion_predictor = EmotionPredictor()
        score, emotion = emotion_predictor.Predict(transform_image)
        cv2.putText(frame, emotion_label[emotion], (0, 100), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 0), 1)

        # Send message (good: 1, 4, 6    bad: 0, 2, 3, 5)
        if IS_NEED_TO_SEND_MESSAGE:
            message = '&Score = ' + str(score) + ', &Emotion = ' + str(emotion) + '\n'
            client.Send(message)
    except:
        print('Exception')

camera = cv2.VideoCapture(1)

detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

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
