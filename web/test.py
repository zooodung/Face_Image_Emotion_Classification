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
example_diary = "오늘 하루 ㄹㅇ 힘들었다. 회사에서 상사한테 ㅈㄴ 혼나고, 팀 프로젝트도 엉망이었음. 점심시간에 잠깐 ㅎㅌㅊ 카페에서 쉬면서 친구한테 카톡으로 털어놨는데, 그래도 조금 나아짐. 퇴근하고 집에 오니 우리 집 강아지가 나를 반겨줘서 그나마 힐링. 요즘 퇴근 후에 넷플릭스 보거나 게임하는데, 뭐 볼지 고민됨. 오늘 밤은 그냥 푹 자고, 내일은 다시 힘내서 출근해야지. 요즘 ㄹㅇ 너무 빡센데, 그래도 화이팅 해야지!"
example_attitude = "공감하기" #조언하기, 공감하기, 위로하기

response = model.generate_response(predicted_emotion, example_diary, example_attitude)

print(f"얼굴로 예상한 감정: {predicted_emotion}")
print(f"댓글 내용: {response}")