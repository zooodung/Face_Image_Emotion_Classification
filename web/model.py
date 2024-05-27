import numpy as np
import cv2
from tensorflow.keras.models import load_model
from mtcnn import MTCNN
import dlib
from openai import OpenAI
import os

client = OpenAI(api_key='none')


#모델 및 디텍터 불러오기
model = load_model('efficientnet_face_emotion.h5')
emotion_labels = ['anger', 'happy', 'panic', 'sadness']
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


#얼굴을 특정
def extract_face_info_mtcnn(img):
    detector = MTCNN()  # MTCNN 인스턴스 생성
    faces = detector.detect_faces(img)  # 얼굴 감지
    for face in faces:
        bounding_box = face['box']  # 바운딩 박스
        keypoints = face['keypoints']  # 특징점
        face_info = {
            'bounding_box': bounding_box,
            'keypoints': keypoints
        }

    return face_info

# 눈을 이용해서 얼굴의 각도를 계산하는 함수
def calculate_angle(face_info):
    left_eye = face_info['keypoints']['left_eye']
    right_eye = face_info['keypoints']['right_eye']

    return np.arctan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0]) * 180 / np.pi


# 이미지를 회전시키는 함수
def rotate_image(image, img_info):
    angle = calculate_angle(img_info)  # 얼굴의 각도 계산
    height, width = image.shape[:2]
    center = (width / 2, height / 2)  # 이미지의 중심
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)  # 회전 매트릭스 생성
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))  # 이미지 회전

    return rotated_image


# 얼굴을 정규화하는 함수
def normalize_face(image, face_info, output_size=(224, 224)):
    landmarks = face_info['keypoints']
    left_eye = np.array(landmarks['left_eye'])
    right_eye = np.array(landmarks['right_eye'])
    nose_tip = np.array(landmarks['nose'])
    eye_distance = np.linalg.norm(left_eye - right_eye)  # 눈 사이 거리 계산
    desired_eye_distance = 0.3 * output_size[0]
    scale = desired_eye_distance / eye_distance  # 스케일링 비율 계산
    M = np.array([[scale, 0, 0], [0, scale, 0]])
    scaled_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))  # 스케일링 적용
    nose_center = nose_tip * scale  # 스케일링된 코 위치
    offset_x = (output_size[0] / 2) - nose_center[0]
    offset_y = (output_size[1] / 2) - nose_center[1]
    M = np.array([[1, 0, offset_x], [0, 1, offset_y]])
    normalized_image = cv2.warpAffine(scaled_image, M, output_size)  # 중심 이동 적용

    return normalized_image

# 이미지를 전처리하는 함수
def preprocess_image(file_bytes):
    npimg = np.frombuffer(file_bytes, np.uint8)  # 파일을 NumPy 배열로 변환
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)  # 이미지를 디코딩
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 이미지를 RGB로 변환
    img_info = extract_face_info_mtcnn(img) # MTCNN을 사용하여 얼굴 정보 추출
    img = rotate_image(img, img_info)  # 이미지 회전
    img = normalize_face(img, img_info)  # 이미지 정규화
    img_array = np.expand_dims(img, axis=-1)  # 채널 차원 추가
    img_array = img_array.astype('float32') / 255.0  # 정규화
    img_array = np.expand_dims(img_array, axis=0)  # 배치 차원 추가
    return img_array

# 감정을 예측하는 함수
def predict_emotion(img_array):

    predictions = model.predict(img_array)  # 예측 수행
    predicted_class = np.argmax(predictions)  # 예측된 클래스 인덱스
    predicted_emotion = emotion_labels[predicted_class]  # 예측된 감정 레이블
    return predicted_emotion

def generate_response(emotion, diary, attitude):
    prompt = f"""
    사용자의 감정과 일기를 보고 답변을 생성하여야함.
    1. 감정과 일기의 내용이 맞지 않으면, 그것을 고려해서 답변함
    2. 태도를 명확히 지켜서 대답해야함
    3. 추상적이고, 일관적인 답변을 하지 않아야함
    4. SNS에 달리는 댓글처럼 답변하여야함

    감정 : {emotion}
    일기 : {diary}
    태도 : {attitude}
    """
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
            {"role": "system", "content": "Your role is to write comments on the posts entered by the person on the site. You must answer in Korean."},
            {"role": "user", "content": prompt}
        ],
        temperature=1
    )

    return response.choices[0].message.content

