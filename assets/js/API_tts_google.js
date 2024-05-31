async function getApiKey() {
    const response = await fetch('assets/js/jsgalvanic-idiom-424916-j8-836fedab9dba.json');
    const data = await response.json();
    return data.private_key; // JSON 파일에서 private_key 값 추출
}

async function play_tts(answer) {
    const apiKey = await getApiKey(); // API 키 가져오기

    const client = new TextToSpeechClient({
      credentials: { private_key: apiKey } // API 키 설정
    });
  
  
    // 텍스트 입력 및 음성 설정
    const text = answer;
    const request = {
      input: { text: text },
      voice: {
        languageCode: 'ko-KR',
        name: 'ko-KR-Wavenet-D'
      },
      audioConfig: { audioEncoding: 'MP3' }
    };
  
    try {
      // 음성 합성 요청
      const [response] = await client.synthesizeSpeech(request);
      const audioContent = response.audioContent;
  
      // 오디오 재생
      const audio = new Audio(`data:audio/mpeg;base64,${audioContent}`);
      audio.play();
    } catch (error) {
      console.error('음성 합성 에러:', error);
    }
  }
  


export {play_tts}
