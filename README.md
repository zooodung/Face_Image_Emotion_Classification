<div align=center>	
 

## ![FaceLog 로고](https://velog.velcdn.com/images/zoodung/post/bb55b2b7-e9e9-476a-80f6-8bdc8dccf209/image.png)<br>얼굴 이미지 감정 분류 모델링<br>Web Service 'FaceLog' Project
</div>

## ✏ 프로젝트 소개

### 얼굴 이미지 감정분류 (😡/😁/😯/😭)

제공받은 IMG DATA/LABEL DATA/SEGMENT DATA로 학습한 머신러닝/딥러닝 모델을 활용해 이미지의 얼굴 객체 인식과 얼굴 객체의 감정을 ANGER/HAPPY/PANIC/SADNESS 분석 및 분류한 후 검증된 성능이 우수한 모델을 선택해 웹 서비스 FaceLog의 입력 데이터 분류에 활용한다.

### FaceLog 
개인용 기밀성 SNS 플랫폼의 프로토타입으로 사용자 정보, 얼굴 이미지, 텍스트, 사용자 맞춤형 프롬프트 설정을 입력받아 멀티모달로 처리 및 저장하며 수집한 정보들을 API Prompt에 입력 및 반영하여 AI 캐릭터 ‘Anna'가 SNS 댓글을 생성해 사용자에게 제공한다. 
사용자가 입력한 모든 데이터와 생성된 데이터는 보호 및 저장되며 메인 프로필 페이지의 캘린더를 통해 언제든지 열람할 수 있다.


## 🕘 프로젝트 기간
**START  : 2024.05.09**
<br>
**END : 2024.06.05**

## 🧑‍💻 팀 구성
- **김성혜** - 발표, 프로젝트 기획, 데이터 EDA, 모델링(VGG19), 모델링(RESNET), 로고 이미지 생성, POST 입력 페이지, 사용자 정보 입력 페이지, 사용자 정보 수정 페이지, 게시물 작성 페이지, 백업 데이터 생성 및 관리
- **박주성** - 형상 관리, 데이터 EDA, 데이터 전처리, 모델링(EmotionNet), 모델링(SVM), 모델링(ViT), 시스템 구성 설계, Fast API 서버 구축, 프롬프트 커스텀 설정 페이지, 사용자 정보 입력 페이지, 사용자 정보 수정 페이지, 메인 프로필 페이지, 게시물 상세 페이지
- **이구협** - 발표, 프로젝트 기획, 모델링(EfficientNet b0), 모델링(EfficientNet b7), 모델링(DeiT), 앙상블 시도, Custom API Prompt 설계, API TTS/STT 구현, Flask 서버 구축, 실시간 채팅 사이드 App 구현, 실시간 채팅 페이지
- **이승후** - 데이터 EDA, 모델링(Resnet), 데이터베이스 연동 시도

## ⌨ 개발 환경
### Language
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/java-F37626?style=for-the-badge&logo=Java&logoColor=white"> 
<img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"> 


### Framework 
<img src="https://img.shields.io/badge/react-61DAFB?style=for-the-badge&logo=react&logoColor=black"> 
<img src="https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white"> 
<img src="https://img.shields.io/badge/tensorflow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white"> 
<img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white"> 

### IDE 
<img src="https://img.shields.io/badge/visual studio code-007ACC?style=for-the-badge&logo=visual studio code&logoColor=white"> 
<img src="https://img.shields.io/badge/jupyter-F37626?style=for-the-badge&logo=Jupyter&logoColor=white"> 

## 🫥 얼굴이미지 감정분류 모델링
### 🔍 EDA
#### Train Data Img counts 
- anger : 1500개 <br>
- happy : 1495개 <br>
- panic : 1501개<br>
- sadness : 1500개
- Sum of ALL : 5996개
#### Validation Data Img counts 
- anger : 300개 <br>
- happy : 300개 <br>
- panic : 300개<br>
- sadness : 300개
- Sum of ALL : 1200개
#### Test Data Img counts 
- anger : 280개 <br>
- happy : 298개 <br>
- panic : 275개<br>
- sadness : 284개<br>
- Sum of ALL : 1137개

#### Train Data Label 데이터 검증
![](https://velog.velcdn.com/images/zoodung/post/a94cf628-efd9-4ed9-99c6-a092b9748878/image.png)
- 0 same, 1same 아웃라이어 판단<br>
- 2 same, 3same 학습 데이터 활용<br>
1. anger : 1118
2. happy : 1474
3. panic : 1102
4. sadness : 1120
>데이터의 균형을 위해 각 감정별 상위 1102개 활용 결정

#### Test Data Label 데이터 검증
![](https://velog.velcdn.com/images/zoodung/post/af8f2bfc-5ad2-4ee8-84ec-4650344f41cc/image.png)<br>
- 목표 성능 **Accuracy** 설정
1. **anger : 73.21%**
2. **happy : 97.65%**
3. **panic : 82.9%**
4. **sadness : 74.64%**
>

### ✂ 전처리
- 얼굴 BOX Crop
  + With Label Data :  Annot_A/B/C의 각 X, Y 좌표의 min, max 값의 각각 평균을 활용해 Crop
  + Without Label Data : Dlib 라이브러리로 얼굴 객체를 인식해 X, Y에 padding 값을 부여하고 Crop
- Left/Right 눈 기준 수평 회전
  - MTCNN 라이브러리를 활용해 얼굴의 특징점을 구하고 좌/우 눈을 기준으로 수평으로 이미지를 회전
- 코끝 기준 중심 이동
  - Dlib 라이브러리를 통해 얻은 얼굴의 특징점중 코끝의 좌표를 이미지의 중심으로 이동
- 눈 사이 거리 값을 정규화
  - Dlib 라이브러리를 통해 얻은 얼굴의 특징점중 눈 사이의 거리를 구하여 정규화를 진행
- 224x224 Resize
  - 모델 학습 및 검증에 입력으로 활용할 이미지의 최종 Output Size는 224x224로 설정한다.
### 🧑‍🏫 모델링 학습
- Imgaug
  1. 이미지 크기 증가
  2. 이미지 위치 이동
  3. 이미지 회전
  4. 이미지 왜곡
- ImageDataGenerator <br>
`    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    zoom_range=0.2,`
> 각 이미지 증강 방법은 모델에 따라 선택적으로 적용
### 🚩 모델링 성능
- VGG19
- ResNet -1
- EmotionNet
- SVM
- ViT b16
- EfficientNet b0
- EfficientNet b7
- DeiT

## 📚 Web Service 'FaceLog'
### 🏁시스템 구성
![](https://velog.velcdn.com/images/zoodung/post/f83aa48f-cf17-4e22-b025-c93722d66dc1/image.png)
> 프로토타입 버전은 데이터베이스에 연동 및 저장하지 않아 서버가 reboot되면 사용자의 입력/생성 정보가 초기화 된다.
### 💡기능
#### 🔴 핵심 기능 1. 사용자 입력 이미지의 감정을 분류
![](https://velog.velcdn.com/images/zoodung/post/eaff22b4-8fde-4274-b490-6a5634d3f647/image.png)
![](https://velog.velcdn.com/images/zoodung/post/1ed6d5b2-cfb0-4278-b2c3-6caf3a730ac0/image.png)
> 현재 ViT_b16 모델을 단일 모델로 활용해 이미지의 감정을 분류하는 상태이며 이후 성능이 향상된 앙상블 모델로 교체할 예정이다. 게시물 작성 페이지를 통해 사용자의 입력을 처리하고 분류된 감정은 UI를 통해 게시물 상세 페이지에서 사용자에게 편리하게 출력한다. 

> 날짜는 오늘의 날짜를 Default 값으로 가지며 이미지나 텍스트를 입력하지 않으면 진행되지 않는다. 얼굴이 드러나지 않은 이미지를 입력한 경우에도 화면에 올바른 이미지 입력을 요구하며 페이지를 reload하고 진행되지 않는다.
#### 🔴 핵심 기능 2. 분류한 감정과 사용자 입력 텍스트를 구조에 맞추어 LLM API Prompt에 입력


```
def generate_response(emotion, inputText, a_attitude, composition, intensity, length, name, introduce):
    emotion_kr = ''
    if (emotion == 'anger'): 
        emotion_kr = '화남'
    elif (emotion == 'happy'): 
        emotion_kr = '기쁨'
    elif (emotion == 'panic'): 
        emotion_kr = '놀람'
    elif (emotion == 'sad'): 
        emotion_kr = '슬픔'

    prompt = f"""
    사용자의 얼굴 감정과 일기를 보고 답변을 생성하여야함.
    1. 태도를 명확히 지켜서 대답해야함.
    2. 추상적이고, 일관적인 답변을 하지 않아야함.
    3. SNS에 달리는 친구의 댓글처럼 답변하여야함.
    4. {a_attitude}로 댓글을 달아야함.
    5. {length}자 내외로 작성하여야함.

    얼굴 감정 : {emotion_kr}
    일기 : {inputText}
    태도 : {composition[0]}, {composition[1]}, {composition[2]} 

    6. 얼굴 감정과 일기에 적힌 내용이 일치하지 않으면, 그것에 대해서 물어야함.
    7. 사용자의 이름은 '{name}'이다. 사용자의 이름을 답변에 포함해야함.
    8. 사용자의 핵심 소개는 '{introduce}'이다. 사용자의 소개를 내용에 참고해야함. 사용자의 소개와 일기가 관련이 없으면 선택적으로 참고함.
    """
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
            {"role": "system", "content": "Your role is to write comments on the posts entered by the person on the site. Emotion is an analysis of a face photo. You must answer in Korean."},
            {"role": "user", "content": prompt}
        ],
        temperature=intensity,
        max_tokens=480,
    )
    # API에서 반환된 텍스트
    text = response.choices[0].message.content
    
    # 얼굴 감정 부분을 제거
    text = text.replace(f"얼굴 감정: {emotion_kr}", "").strip()

    return text
```
#### 🔴 핵심 기능 3. LLM API를 통해 답변을 생성
![](https://velog.velcdn.com/images/zoodung/post/7b75379b-ece0-49ec-9c8d-c70263344f6b/image.png)
#### 🔴 핵심 기능 4. 입력/생성한 데이터를 저장해 열람 가능하게 함.
![](https://velog.velcdn.com/images/zoodung/post/666eb33b-a36c-4d5c-95eb-d213ab936f2f/image.png)
#### 🔴 핵심 기능 5. 출력 구조에 맞추어 SNS 댓글 형식으로 웹페이지에 출력
![](https://velog.velcdn.com/images/zoodung/post/07723b42-630f-4bcc-950f-ca0cea84330a/image.png)
#### 🟡 부가 기능 1. 사용자 맞춤형 LLM API Prompt 설정
![](https://velog.velcdn.com/images/zoodung/post/68c10c82-fe55-4f10-a3a9-e01d173d9331/image.png)
> 사용자는 대화 태도, 답변 구성, 답변 길이를 필수로 한가지 선택해야하며 선택하지 않을시 진행되지 않는다. 
답변 구성은 복수로 선택할 수 있으며 아무것도 선택하지 않을시 조언, 위로, 공감을 모두 선택한 것으로 간주한다.
#### 🟡 부가 기능 2. 사용자 생성 및 정보(이름, 소개) 입력 LLM API Prompt에 반영
![](https://velog.velcdn.com/images/zoodung/post/c85cdc10-6092-42c8-b903-45b58f91c7ad/image.png)
```
7. 사용자의 이름은 '{name}'이다. 사용자의 이름을 답변에 포함해야함.
8. 사용자의 핵심 소개는 '{introduce}'이다. 사용자의 소개를 내용에 참고해야함. 사용자의 소개와 일기가 관련이 없으면 선택적으로 참고함.
```
>사용자 이름은 필수적으로 입력을 요구하며 소개는 사용자가 선택해 입력하거나 입력하지 않을 수 있다.
#### 🟡 부가 기능 3. TTS 
![](https://velog.velcdn.com/images/zoodung/post/5c831ab1-8db5-4d2c-b6b4-bfb18f718974/image.png)
>스피커 이미지 버튼을 클릭하면 생성된 댓글의 텍스트를 TTS를 통해 음성으로 재생한다.
#### 🟡 부가 기능 4. 사용자 정보 수정
![](https://velog.velcdn.com/images/zoodung/post/eec970c2-7e53-4d9a-92ab-4316991b6f76/image.png)
>기존에 생성되었던 사용자의 정보에서 이름과 소개만을 Update하며 작성한 게시물의 내역은 유지한다.
#### 🟡 부가 기능 5. STT
![](https://velog.velcdn.com/images/zoodung/post/aaff6c42-1065-423b-adc8-0270f1f39c31/image.png)
>사이드 App인 실시간 채팅을 통해 구현되어 있으며 게시물 작성 페이지에도 해당 기능을 추가할 예정이다. 마이크 이미지 버튼을 누르면 녹음을 시작하고 다시 한번 누르면 녹음을 중단한다. 
#### 🟡 부가 기능 6. 누적 감정 카운트
![](https://velog.velcdn.com/images/zoodung/post/69551b45-0771-44c6-b131-68ae9f8557cb/image.png)
>상용 서비스의 게시물 수, 팔로잉, 팔로워 기능을 참고했으며 기존에 작성되었던 게시물들의 감정 분류 결과를 누적 카운트 수를사용자에게 보기 쉽게 출력한다.

### 💻 화면 구성
#### ✨ 사용자 정보 입력 페이지
![](https://velog.velcdn.com/images/zoodung/post/d723d69f-b707-4266-b6fa-5910b9a12f79/image.png)
>사용자의 이름을 필수로 입력받고 소개는 선택적으로 입력받으며 'GET PROFILE' 버튼을 클릭하면 사용자 프로필을 생성한다.
#### ✨ 프롬프트 커스텀 설정 페이지
![](https://velog.velcdn.com/images/zoodung/post/bcc77a8e-a650-48ae-8fb2-b1ba1d440055/image.png)
>사용자는 대화 태도, 답변 강도, 답변 길이를 필수적으로 선택해야 하며 답변 구성은 선택하지 않을시 조언, 위로, 공감 모두 선택한 것으로 간주한다.

>답변 강도는 생성 과정의 Temperature Value를 의미하며 창의적(1.0), 보통(0.75), 정적(0.5)의 값을 가진다.

>답변 길이는 짧게(150자 내외), 보통(300자 내외), 길게(450자 내외)의 값을 가진다.
#### ✨ 메인 프로필 페이지
![](https://velog.velcdn.com/images/zoodung/post/af8174bd-cf06-4ba6-9715-c50a540d6013/image.png)
>'NEW POST' 버튼을 클릭해 게시물 작성 페이지에 진입할 수 있다.

>'AI SETTING' 버튼을 클릭해 프롬프트 커스텀 설정 페이지에 재진입할 수 있다.

>프로필 이름 출력 우측의 '설정 이미지 버튼' 을 클릭해 사용자 정보 수정 페이지에 진입할 수 있다.

>'My Emotions' 누적 감정 카운트 출력 위의 'DM 이미지 버튼' 을 클릭해 RealTime ChatApp 페이지에 진입할 수 있다.

>'CALENDAR' 의 원하는 Month를 클릭하면 생성 및 저장되어 있는 사용자의 정보를 탐색해 해당하는 Month의 게시물 버튼을 생성하며 기존에 작성되어 있는 게시물을 확인할 수 있고, 게시물을 클릭하면 게시물 상세 페이지로 진입할 수 있다.

> 클릭한 Month에 해당하는 정보가 없으면 '데이터가 없음'을 출력한다.

#### ✨ 사용자 정보 수정 페이지 
![](https://velog.velcdn.com/images/zoodung/post/7b0730c7-90d8-4a76-b69c-4de01e139044/image.png)
>이름을 필수적으로 입력받고 소개는 선택적으로 입력받는다.

>기존에 생성된 클래스에 Update하며 기존에 작성 및 저장된 게시물 내역은 유지한다.
#### ✨ 게시물 작성 페이지
![](https://velog.velcdn.com/images/zoodung/post/5d38132c-83eb-4172-b36b-2846f4957016/image.png)
> 이미지, 연도, 월, 날짜, 텍스트의 입력을 요구한다.

> 하나의 필드라도 입력되지 않으면 진행되지 않는다.

> 얼굴이 드러나지 않은 잘못된 이미지를 입력하면 화면에 2.5초간 '이미지에서 얼굴을 인식하지 못했습니다. 얼굴이 드러난 이미지를 업로드해주세요!' 를 출력한다.
#### ✨ 게시물 상세 페이지
![](https://velog.velcdn.com/images/zoodung/post/861ed63b-8b3d-4ca0-838b-d8e039cd5c89/image.png)
> 입력 이미지 데이터, 감정 분류 결과, 입력 텍스트 데이터, 입력 날짜 데이터를 사용자 필드에 출력하고 AI 필드에는 AI 캐릭터 'Anna'와 생성된 답변 텍스트를 출력한다. 

> 오른쪽 하단의 '스피커 이미지 버튼'을 클릭하면 TTS 기능이 실행되며 생성된 텍스트를 음성으로 재생한다.

