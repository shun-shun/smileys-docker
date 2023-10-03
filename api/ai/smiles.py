from feat import Detector
import numpy as np
from PIL import Image
import random

detector = Detector(
    face_model="retinaface",
    landmark_model="mobilefacenet",
    au_model='svm', # ['svm', 'logistic', 'jaanet']
    emotion_model="resmasknet",
)


def start(img):

    image_prediction = detector.detect_image(img,batch_size = 200,face_detection_threshold = 0.7,face_identity_threshold = 0.9)
        
    #感情に関するカラムだけを残す
    image_prediction = image_prediction[["FaceRectX","FaceRectY","happiness"]]
    result = image_prediction.values
    
    # 先頭を取得(精度良すぎ)
    result = result[:1]
    # 末尾を取得(精度悪い)
    # result = result[-1:]

    # 50％未満の場合はランダム(61％〜79％の間)で上方変換する
    if np.less(result[0][2], np.array([0.5])):
        y = np.array([random.uniform(0.61, 0.79)])
        result[0][2] = y
        print("上方変換")

    if(random.random() > 0.95) :
        print("変換なし")
        return result.tolist()

    # 90％以上の場合はランダム(81%〜93％の間)で下方変換する
    if np.greater_equal(result[0][2], np.array([0.9])):
        y = np.array([random.uniform(0.81, 0.93)])
        result[0][2] = y
        print("下方変換")

    #print(image_prediction.to_json(orient='records'))
    return result.tolist()