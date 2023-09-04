from feat import Detector
import numpy as np

detector = Detector(
    face_model="retinaface",
    landmark_model="mobilefacenet",
    au_model='svm', # ['svm', 'logistic', 'jaanet']
    emotion_model="resmasknet",
)

def start(img):
    image_prediction = detector.detect_image(img)
        
    #感情に関するカラムだけを残す
    image_prediction = image_prediction[["FaceRectX","FaceRectY","happiness"]]
        
    #print(image_prediction.to_json(orient='records'))
    return image_prediction.values.tolist()