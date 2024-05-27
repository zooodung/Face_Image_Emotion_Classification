import model
import cv2
import numpy as np

test_image_path = 'test_img/test_image.jpg'

#전처리 (웹에서 받는 이미지와 동일한 형식을 유지하게)
def load_test_image(image_path):
    img = cv2.imread(image_path)
    _, img_encoded = cv2.imencode('.jpg', img)
    file_bytes = np.array(img_encoded).tobytes()
    return file_bytes



# 테스트 이미지 로드
file_bytes = load_test_image(test_image_path)

# 이미지 전처리 및 감정 예측
img_array = model.preprocess_image(file_bytes)
predicted_emotion = model.predict_emotion(img_array)

# 예제 일기와 태도
example_diary = "오늘은 정말 행복한 날이었다. 친구들과 함께 놀이공원에 갔는데, 모두들 웃고 즐거워했다. 놀이기구를 타고, 맛있는 음식을 먹으며 행복한 시간을 보냈다. 이 순간들이 계속되길 바란다."
example_attitude = "조언하기" #조언하기, 공감하기, 위로하기

response = model.generate_response(predicted_emotion, example_diary, example_attitude)

print(f"얼굴로 예상한 감정: {predicted_emotion}")
print(f"댓글 내용: {response}")