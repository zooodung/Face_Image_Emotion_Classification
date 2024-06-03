import tensorflow as tf
import numpy as np
import dlib
import cv2
from mtcnn import MTCNN
import matplotlib.pyplot as plt
import sys
import os
from tensorflow.keras.models import load_model

vit_model = tf.saved_model.load(r"C:\Users\박주성\Desktop\finalproject\web\web\model\ViT_b16")
#eff = load_model(r'C:\Users\박주성\Desktop\finalproject\web\model\efficientnet_face_emotion_new.h5')


# 얼굴만 크롭하는 함수
def cropface_dlib(image, padding=100):
    detector = dlib.get_frontal_face_detector()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face_index, face in enumerate(faces):
        x, y, w, h = face.left(), face.top(), face.width(), face.height()

        # Add padding
        x -= padding
        y -= padding
        w += padding * 2
        h += padding * 2

        # Ensure the bounding box is within the image boundaries
        x = max(0, x)
        y = max(0, y)
        w = min(image.shape[1] - x, w)
        h = min(image.shape[0] - y, h)

        face_image = image[y:y+h, x:x+w]

    return face_image

# mtcnn으로 얼굴의 특징점을 추출하는 함수 
def extract_faceinfo_mtcnn(img):
    detector = MTCNN()
    faces = detector.detect_faces(img) # 얼굴 감지
    #face_info_list = [] # 감지된 얼굴 정보를 저장할 리스트 // 하나의 이미지에 다수의 얼굴이 존재할 경우 사용

    for face in faces:
        # 얼굴의 바운딩 박스와 특징점 추출
        bounding_box = face['box']
        keypoints = face['keypoints']

        # 추출한 정보를 딕셔너리로 저장
        face_info = {
            'bounding_box': bounding_box,
            'keypoints': keypoints
        }

        # 얼굴 정보 리스트에 추가
        #face_info_list.append(face_info)

    return face_info

# 회전할 각도를 계산하는 함수
def calculate_angle(face_info):
  left_eye = face_info['keypoints']['left_eye']
  right_eye = face_info['keypoints']['right_eye']

  return np.arctan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0]) * 180 / np.pi

# 양쪽 눈을 수평으로 이미지를 회전하는 함수
def rotate_image(image, img_info):
  angle = calculate_angle(img_info)
  # 이미지의 중심 탐색
  height, width = image.shape[:2]
  center = (width / 2, height / 2)

  # 회전 변환 매트릭스 생성
  rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

  # 이미지 회전
  rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

  return rotated_image

# 코끝을 이미지의 가운데로 이동시키고 눈 사이를 스케일링 하는 함수
def normalize_face(image, face_info, output_size=(224, 224)):
    landmarks = face_info['keypoints']
    left_eye = np.array(landmarks['left_eye'])
    right_eye = np.array(landmarks['right_eye'])
    nose_tip = np.array(landmarks['nose'])

    # 눈 사이 거리
    eye_distance = np.linalg.norm(left_eye - right_eye)

    # 스케일링 비율
    desired_eye_distance = 0.3 * output_size[0]
    scale = desired_eye_distance / eye_distance

    # 눈 사이 거리 정규화
    M = np.array([[scale, 0, 0], [0, scale, 0]])
    scaled_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

    # 코 끝을 기준으로 중심 이동
    nose_center = nose_tip * scale
    offset_x = (output_size[0] / 2) - nose_center[0]
    offset_y = (output_size[1] / 2) - nose_center[1]
    M = np.array([[1, 0, offset_x], [0, 1, offset_y]])
    normalized_image = cv2.warpAffine(scaled_image, M, output_size)

    return normalized_image

def classificate_emotion(path):
    emotion_labels = ['anger', 'happy', 'panic', 'sadness']
    # 이미지 로드
    image = cv2.imread(path)

    #if image is None:
    #    print(f"Error: Could not read image from '{path}'")
    
    # 전처리
    image = cropface_dlib(image) # 얼굴 crop

    try:
        face_info = extract_faceinfo_mtcnn(image) # 얼굴 특징점 추출
        image = rotate_image(image, face_info) # 눈 수평 회전
        image = normalize_face(image, face_info) # 코 가운데 이동, 눈 사이 스케일링

        # 이미지를 모델에 전달하여 예측 수행
        img_array = np.expand_dims(image, axis=0)  # 마지막 차원에 채널 추가
        img_array = img_array.astype('float32') / 255.0  # 0~1 사이 값으로 정규화

        # 감정 분류
        predictions = vit_model(img_array)
        predicted_class = np.argmax(predictions)
        predicted_emotion = emotion_labels[predicted_class]
    except Exception as e:
        image = cv2.resize(image, (224, 224)) # 리사이징
        img_array = np.expand_dims(image, axis=0)  # 마지막 차원에 채널 추가
        img_array = img_array.astype('float32') / 255.0  # 0~1 사이 값으로 정규화

        # 감정 분류
        predictions = vit_model(img_array)
        predicted_class = np.argmax(predictions)
        predicted_emotion = emotion_labels[predicted_class]
    
    return predicted_emotion

#dir_path = r"images/"
#filename = r"4jk32a571aebe359e47e4d43744109a48df2725457c51c424edfddd69ae587i6v.jpg"
#emotion = classificate_emotion(dir_path+filename)
#print(f"Emotion: {emotion}")
