import openai

client = openai.OpenAI(api_key='API_KEY') 

#if (aicharacter == 'Anna'):
#    ai_concept = "20대 여성이 자주 사용하는 말투와 단어, 유행어, 줄임말 등을 선택하고 여성들의 대화 특징을 매우 두드러지게 표현해야함."
#elif(aicharacter == 'Kevin'):
#    ai_concept = "20대 남성이 자주 사용하는 말투와 단어, 유행어, 줄임말 등을 선택하고 남성들의 대화 특징을 매우 두드러지게 표현해야함."
#    6. {ai_concept}

conversation_history = []

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

    6.얼굴 감정과 일기에 적힌 내용이 일치하지 않으면, 그것에 대해서 물어야함.
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

#text = generate_response('sad', '오늘 내가 응원하는 야구 팀이 1점도 내지 못하고 무기력하게 졌어. 오늘까지만 해도 9연패야. 저게 연봉 받으면서 야구하는 프로 선수들이 맞을까 궁금할 정도로 수준이 떨어지는 것 같더라. 응원한지 10년째인데 이제 다른 팀을 응원해야되나 싶어.' )

#print(f'AI answer: {text.strip('"')}')

#stt를 불러오는 함수
def stt_function(audio_file_path):
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            transcript = transcription.text 
            return transcript
    except FileNotFoundError:
        return "Audio file not found."

def talk_to_gpt(prompt, conversation_history=[]):
    """
    주어진 프롬프트를 사용하여 GPT-4o 모델과 대화합니다.
    """
    conversation_history.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Your role is to talk to the user in real time. You must answer in Korean."}] + conversation_history,
        temperature=0.9,
    )
    
    reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": reply})
    
    return reply, conversation_history

def generate_first_response(emotion):
    if emotion == 'anger':
        prompt = "사용자는 지금 화가 난 상태입니다. 무슨일이 있었는지 물어봐야함."
    elif emotion == "happy":
        prompt = "사용자는 지금 행복한 상태입니다. 무슨일이 있었는지 물어봐야함."
    elif emotion == "sad":
        prompt = "사용자는 지금 슬픈 상태입니다. 무슨일이 있었는지 물어봐야함."
    elif emotion == "panic":
        prompt = "사용자는 지금 놀란 상태입니다. 무슨일이 있었는지 물어봐야함."
    else:
        prompt = "사용자의 감정을 분석할 수 없음. 평범한 인삿말을 건내야함."

    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
            {"role": "system", "content": "Your role is to talk to the user in real time. Emotion is an analysis of a face photo. You must answer in Korean."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=400,
    )

    print(response.choices[0].message.content)

    return response.choices[0].message.content