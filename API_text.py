import openai

client = openai.OpenAI(api_key='apikeys') 

#if (aicharacter == 'Anna'):
#    ai_concept = "20대 여성이 자주 사용하는 말투와 단어, 유행어, 줄임말 등을 선택하고 여성들의 대화 특징을 매우 두드러지게 표현해야함."
#elif(aicharacter == 'Kevin'):
#    ai_concept = "20대 남성이 자주 사용하는 말투와 단어, 유행어, 줄임말 등을 선택하고 남성들의 대화 특징을 매우 두드러지게 표현해야함."
#    6. {ai_concept}


def generate_response(emotion, inputText):
    emotion_kr = ''
    attitude = ''
    if (emotion == 'anger'): 
        emotion_kr = '화남'
        attitude = '공감하기, 위로하기'
    elif (emotion == 'happy'): 
        emotion_kr = '기쁨'
        attitude = '공감하기, 조언하기'
    elif (emotion == 'panic'): 
        emotion_kr = '놀람'
        attitude = '공감하기, 조언하기'
    elif (emotion == 'sad'): 
        emotion_kr = '슬픔'
        attitude = '공감하기, 위로하기'

    prompt = f"""
    사용자의 얼굴 감정과 일기를 보고 답변을 생성하여야함.
    1. 태도를 명확히 지켜서 대답해야함.
    2. 추상적이고, 일관적인 답변을 하지 않아야함.
    3. SNS에 달리는 댓글처럼 답변하여야함.
    4. 친구처럼 반말로 댓글을 달아야함.
    5. 300자 내외로 작성하여야함.

    얼굴 감정 : {emotion_kr}
    일기 : {inputText}
    태도 : {attitude}

    6.얼굴 감정과 일기에 적힌 내용이 일치하지 않으면, 그것에 대해서 물어야함.
    """
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
            {"role": "system", "content": "Your role is to write comments on the posts entered by the person on the site. Emotion is an analysis of a face photo. You must answer in Korean."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=350,
    )

    # API에서 반환된 텍스트
    text = response.choices[0].message.content
    
    # 얼굴 감정 부분을 제거
    text = text.replace(f"얼굴 감정: {emotion_kr}", "").strip()

    return text

#text = generate_response('sad', '오늘 내가 응원하는 야구 팀이 1점도 내지 못하고 무기력하게 졌어. 오늘까지만 해도 9연패야. 저게 연봉 받으면서 야구하는 프로 선수들이 맞을까 궁금할 정도로 수준이 떨어지는 것 같더라. 응원한지 10년째인데 이제 다른 팀을 응원해야되나 싶어.' )

#print(f'AI answer: {text.strip('"')}')