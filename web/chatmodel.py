from pydub import AudioSegment
from pathlib import Path
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from mtcnn import MTCNN
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

#모델 및 디텍터 불러오기
emotion_model = load_model('efficientnet_face_emotion.h5')
emotion_labels = ['화남', '행복', '놀람', '슬픔']

#stt를 불러오는 함수
def stt_function(audio_file):
    """
    주어진 오디오 파일을 텍스트로 변환합니다.
    """
    audio_file= open("input.mp3", "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    return transcription.text

def talk_to_gpt(prompt):
    """
    주어진 프롬프트를 사용하여 GPT-4o 모델과 대화합니다.
    """
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
            {"role": "system", "content": "Your role is to talk to the user in real time. You must answer in Korean."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=400,
    )
    gpt_Response = response.choices[0].message.content
    return gpt_Response

def tts_function(text):
    """
    주어진 텍스트를 음성 파일로 변환합니다.
    """

    response = client.audio.speech.create(
        model="tts-1",
        input=text,
        voice="nova",
        response_format="mp3",
        speed=1.0,
    )

    return response.stream_to_file("output.mp3")

def extract_face_info_mtcnn(img):
    """
    MTCNN을 사용하여 얼굴 정보를 추출합니다.
    """
    detector = MTCNN()
    faces = detector.detect_faces(img)
    for face in faces:
        bounding_box = face['box']
        keypoints = face['keypoints']
        face_info = {
            'bounding_box': bounding_box,
            'keypoints': keypoints
        }
    return face_info

def calculate_angle(face_info):
    """
    눈을 이용해서 얼굴의 각도를 계산합니다.
    """
    left_eye = face_info['keypoints']['left_eye']
    right_eye = face_info['keypoints']['right_eye']
    return np.arctan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0]) * 180 / np.pi

def rotate_image(image, img_info):
    """
    이미지를 회전시킵니다.
    """
    angle = calculate_angle(img_info)
    height, width = image.shape[:2]
    center = (width / 2, height / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    return rotated_image

def normalize_face(image, face_info, output_size=(224, 224)):
    """
    얼굴을 정규화합니다.
    """
    landmarks = face_info['keypoints']
    left_eye = np.array(landmarks['left_eye'])
    right_eye = np.array(landmarks['right_eye'])
    nose_tip = np.array(landmarks['nose'])
    eye_distance = np.linalg.norm(left_eye - right_eye)
    desired_eye_distance = 0.3 * output_size[0]
    scale = desired_eye_distance / eye_distance
    M = np.array([[scale, 0, 0], [0, scale, 0]])
    scaled_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    nose_center = nose_tip * scale
    offset_x = (output_size[0] / 2) - nose_center[0]
    offset_y = (output_size[1] / 2) - nose_center[1]
    M = np.array([[1, 0, offset_x], [0, 1, offset_y]])
    normalized_image = cv2.warpAffine(scaled_image, M, output_size)
    return normalized_image

def preprocess_image(file_bytes):
    """
    이미지를 전처리합니다.
    """
    npimg = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_info = extract_face_info_mtcnn(img)
    img = rotate_image(img, img_info)
    img = normalize_face(img, img_info)
    img_array = np.expand_dims(img, axis=-1)
    img_array = img_array.astype('float32') / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_emotion(img_array):
    """
    감정을 예측합니다.
    """
    predictions = emotion_model.predict(img_array)
    predicted_class = np.argmax(predictions)
    predicted_emotion = emotion_labels[predicted_class]
    return predicted_emotion

def generate_first_responce(emotion):
    if emotion == '화남':
        prompt = "사용자는 지금 화가 난 상태입니다. 무슨일이 있었는지 물어봐야함."
    elif emotion == "행복":
        prompt = "사용자는 지금 행복한 상태입니다. 무슨일이 있었는지 물어봐야함."
    elif emotion == "슬픔":
        prompt = "사용자는 지금 슬픈 상태입니다. 무슨일이 있었는지 물어봐야함."
    elif emotion == "놀람":
        prompt = "사용자는 지금 놀란 상태입니다. 무슨일이 있었는지 물어봐야함."
    else:
        prompt = "사용자의 감정을 분석할 수 없음. 평범한 인삿말을 건내야함."

    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
            {"role": "system", "content": "Your role is to write comments on the posts entered by the person on the site. Emotion is an analysis of a face photo. You must answer in Korean."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=400,
    )

    return response.choices[0].message.content