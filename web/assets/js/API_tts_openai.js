async function generateSpeech(text) {
    const apiKey = "API_KEY"; 
    const url = "https://api.openai.com/v1/audio/speech";
  
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: "tts-1", // 모델 선택
        voice: "nova", // 음성 선택
        input: text
      })
    });
  
    if (response.ok) {
      const blob = await response.blob();
      const audioUrl = URL.createObjectURL(blob);
      
      // 오디오 재생
      const audio = new Audio(audioUrl);
      audio.play();
  
      // 또는, 오디오 파일 다운로드 링크 생성
      //const link = document.createElement("a");
      //link.href = audioUrl;
      //link.download = "output.mp3";
      //link.click();
    } else {
      const errorData = await response.json();
      console.error("Error:", errorData);
    }
}

export {generateSpeech}

  // 사용 예시
  //generateSpeech("안녕하세요, OpenAI TTS API를 사용하여 음성을 생성합니다.");