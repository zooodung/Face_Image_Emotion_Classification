import { generateSpeech } from './API_tts_openai.js';

let recorder;
let isRecording = false;
let responseText; // 전역 변수로 response_text 저장
let recordedAudioBlob; // 녹음된 오디오 데이터를 저장할 변수

document.getElementById('upload-btn').addEventListener('click', async function() {
    try {
        responseText = await uploadImage();
        console.log('Response Text:', responseText);
        displayResponse(responseText); // 말풍선 출력 함수 호출
        generateSpeech(responseText)
        .then(() => {
            console.log('TTS 재생 완료');
        })
        .catch(error => {
            // 에러 처리
            console.error('TTS 재생 실패:', error);
        });
    } catch (error) {
        console.error('Error:', error);
    }
});

document.getElementById('recordButton').addEventListener('click', async function() {
    try {
      responseText = await toggleRecording();
      console.log('Response Text:', responseText);
      displayResponse(responseText); // 말풍선 출력 함수 호출
  
      // TTS 재생 (await 사용)
      try {
        await generateSpeech(responseText);
        console.log('TTS 재생 완료');
      } catch (error) {
        console.error('TTS 재생 실패:', error);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  });

function displayResponse(text) {
    const chatContainer = document.getElementById('chat-container');
    const chatBubble = document.createElement('div');
    chatBubble.classList.add('chat-bubble');
    chatBubble.textContent = text;
    chatContainer.appendChild(chatBubble);
}

function uploadImage() {
    const imageInput = document.getElementById('imageInput');
    const file = imageInput.files[0];
    const formData = new FormData();
    formData.append('image', file);
  
    // Display the uploaded image
    const imageDisplay = document.getElementById('imageDisplay');
    imageDisplay.src = URL.createObjectURL(file);
  
    return fetch('/upload_chat_image', { // fetch 결과 반환
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Image uploaded successfully:', data);
        return data.response;  // response_text 대신 response를 반환
    })
    .catch(error => console.error('Error uploading image:', error));
  }

function toggleRecording() {
    const recordIcon = document.getElementById('recordIcon');
  
    if (!isRecording) {
      // 녹음 시작
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
          recorder = new MediaRecorder(stream);
          recorder.start();
          recordIcon.src = "https://upload.wikimedia.org/wikipedia/commons/b/b3/Circle-icons-stop.svg";
          isRecording = true;
        })
        .catch(error => console.error("Error getting audio stream:", error));
    } else {
        // 녹음 중지
        recorder.stop();
        recorder.ondataavailable = e => {
            const audioBlob = e.data;
            const formData = new FormData();
            formData.append('audio', audioBlob, 'input.mp3');

            fetch('/record_audio', {
            method: 'POST',
            body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok.');
                }
                return response.json();
            })
            .catch(error => console.error("Error recording audio:", error));

            recordIcon.src = "https://upload.wikimedia.org/wikipedia/commons/7/7c/Circle-icons-microphone.svg";
            isRecording = false;
      };
    }
}