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

  async function toggleRecording() {  // 함수에 async 추가
    const recordIcon = document.getElementById('recordIcon');

    if (!isRecording) {
        try {  // 에러 처리를 위해 try-catch 블록 추가
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });  // async/await 사용
            recorder = new MediaRecorder(stream);
            recorder.start();
            recordIcon.src = "https://upload.wikimedia.org/wikipedia/commons/b/b3/Circle-icons-stop.svg";
            isRecording = true;

            return new Promise((resolve) => {  // Promise 반환
                recorder.ondataavailable = async (e) => {
                    const audioBlob = e.data;
                    const formData = new FormData();
                    formData.append('audio', audioBlob, 'input.mp3');

                    try {  // 에러 처리를 위해 try-catch 블록 추가
                        const response = await fetch('/record_audio', {  // async/await 사용
                            method: 'POST',
                            body: formData
                        });

                        if (!response.ok) {  // 네트워크 응답 확인
                            throw new Error('Network response was not ok.');
                        }

                        const data = await response.json();
                        resolve(data.response);  // Promise resolve
                    } catch (error) {  // 에러 처리
                        console.error("Error recording audio:", error);
                        resolve("Error recording audio");  // 에러 발생 시에도 Promise resolve
                    }

                    recordIcon.src = "https://upload.wikimedia.org/wikipedia/commons/7/7c/Circle-icons-microphone.svg";
                    isRecording = false;
                };
            });
        } catch (error) {  // 에러 처리
            console.error("Error getting audio stream:", error);
            return "Error getting audio stream";
        }
    } else {
        // 녹음 중지
        recorder.stop();
    }
}