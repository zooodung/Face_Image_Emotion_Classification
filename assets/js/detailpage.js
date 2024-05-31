import { ai_Anna, ai_Kevin, ai_Drake } from './AI_Profile.js';
import { generateSpeech } from './API_tts_openai.js';
//import {play_tts} from './API_tts_google.js'
import { synthesizeSpeech } from './API_tts_eleven.js'

document.addEventListener('DOMContentLoaded', () => {
  // 쿼리 파라미터 가져오기 (null 체크 추가)
  const urlParams = new URLSearchParams(window.location.search);
  const text = urlParams.get('text') || '';
  const date = urlParams.get('date') || '';
  const emotion = urlParams.get('emotion') || '';
  const year = urlParams.get('year') || '';
  const month = urlParams.get('month') || '';
  const aicharacter = urlParams.get('aicharacter') || '';
  const aianswer = urlParams.get('aianswer') || '';
  const imgpath = urlParams.get('imagepath') || '';

  console.log("imagepath:", imgpath);
  console.log("year:", year);
  console.log("month:", month);
  console.log("date:", date);
  console.log("text:", text);
  console.log("emotion:", emotion);
  console.log("aicharacter:", aicharacter);
  console.log("aianswer:", aianswer);
  

  let aiProfiles = []; // aiProfiles 변수를 전역 범위로 이동
  
  if (aicharacter === 'Anna') {
    aiProfiles = [ai_Anna];
  } else if (aicharacter === 'Kevin') {
    aiProfiles = [ai_Kevin];
  } else if (aicharacter === 'Drake') {
    aiProfiles = [ai_Drake];
  } else {
    aiProfiles = [ai_Anna]; // 기본값 설정
  }

  let textToDisplay = text;
  const profileImagePath = imgpath;

  // AI 프로필 배열 생성
  //const aiProfilesOptions = [
  //  [ai_Anna, ai_Kevin, ai_Drake],
  //  [ai_Anna, ai_Kevin],
  //  [ai_Anna]
  //];

  // 랜덤하게 세 문장 중 하나 선택
  //const selectedOption = aiProfilesOptions[Math.floor(Math.random() * aiProfilesOptions.length)];

  // 시간 형식 수정
  const timeDisplay = document.querySelector('.logtime');
  timeDisplay.textContent = `${year}년 ${month}월 ${date}일 `; 

  // 감정 및 이미지, 텍스트 표시 영역 가져오기
  const emotionDisplay = document.getElementById("emotion-display");
  const imageDisplay = document.getElementById("black-box2");
  const textDisplay = document.getElementById("text-display");

  // 감정에 따라 색상 및 이미지 설정
  function updateEmotionDisplay(emotion) {
    emotionDisplay.textContent = emotion; 

    let imagePath = "";
    if (emotion === "happy") {
      emotionDisplay.style.color = 'rgba(247, 243, 2, 0.747)';
      imagePath = "assets/images/happy.png";
    } else if (emotion === "anger") {
      emotionDisplay.style.color = 'rgba(228, 91, 91, 0.801)';
      imagePath = "assets/images/anger.png";
    } else if (emotion === "panic") {
      emotionDisplay.style.color = 'rgb(77, 158, 97)';
      imagePath = "assets/images/panic.png";
    } else if (emotion === "sad") {
      emotionDisplay.style.color = 'rgb(99, 150, 226)';
      imagePath = "assets/images/sad.png";
    }

    if (imagePath) {
      imageDisplay.innerHTML = `<img src="${imagePath}" alt="${emotion}">`;
    } else {
      imageDisplay.innerHTML = '';
    }

    textDisplay.textContent = textToDisplay;
    textDisplay.scrollTop = 0; 
  }

  // 초기 표시
  updateEmotionDisplay(emotion);

  // 프로필 이미지 설정
  const profileImageDisplay = document.getElementById("empty-square");
  const profileImage = new Image();
  profileImage.src = profileImagePath;
  profileImage.onload = () => {
    profileImage.width = 224;
    profileImage.height = 224;
    profileImageDisplay.appendChild(profileImage);
  };

  const aiContainersWrapper = document.querySelector('.ai-containers-wrapper');
  const buttonImages = [
    'assets/images/like_button.png',
    'assets/images/hate_button.png',
  ];

  // ai-containers-wrapper의 자식 요소들을 모두 제거
  while (aiContainersWrapper.firstChild) {
    aiContainersWrapper.removeChild(aiContainersWrapper.firstChild);
  }

  // AI 프로필 정보를 이용하여 컨테이너 생성
  aiProfiles.forEach((aiProfile) => { 
    const aiContainer = document.createElement('div');
    aiContainer.classList.add('ai-container');

    // 위쪽 컨테이너
    const topContainer = document.createElement('div');
    topContainer.classList.add('top-container');

    const aiEmptyContainer1 = document.createElement('div');
    aiEmptyContainer1.classList.add('ai-empty-container1');

    const aiProfileImage = new Image();
    aiProfileImage.src = aiProfile.profileimg; 
    aiProfileImage.onload = () => {
      aiProfileImage.width = 180;
      aiProfileImage.height = 180;
      aiEmptyContainer1.appendChild(aiProfileImage);
    };

    const aiEmptyContainer2 = document.createElement('div');
    aiEmptyContainer2.classList.add('ai-empty-container2');
    aiEmptyContainer2.scrollTop = 0; 

    // aiEmptyContainer2에 aianswer 추가
    const aiAnswerElement = document.createElement('span');
    aiAnswerElement.textContent = aianswer; 
    aiEmptyContainer2.appendChild(aiAnswerElement);

    topContainer.appendChild(aiEmptyContainer1);
    topContainer.appendChild(aiEmptyContainer2);

    // 아래쪽 컨테이너
    const bottomContainer = document.createElement('div');
    bottomContainer.classList.add('bottom-container');

    const aiEmptyContainer3 = document.createElement('div');
    aiEmptyContainer3.classList.add('ai-empty-container3');

    const nameElement = document.createElement('span');
    nameElement.textContent = aiProfile.name;
    aiEmptyContainer3.appendChild(nameElement);

    bottomContainer.appendChild(aiEmptyContainer3);

    // 버튼 이미지 생성 및 추가
    buttonImages.forEach((buttonImage, buttonIndex) => {
      const button = document.createElement('button');
      button.classList.add(buttonIndex === 0 ? 'like-button' : 'hate-button');

      const img = document.createElement('img');
      img.src = buttonImage;
      img.alt = buttonIndex === 0 ? '좋아요 버튼' : '싫어요 버튼';
      img.style.width = '30px';
      img.style.height = '30px';

      button.appendChild(img);
      bottomContainer.appendChild(button);

      /*button.addEventListener('click', () => {
        if (buttonType === 'like') {
            aiProfile.increaseLike();
        } else if (buttonType === 'hate') {
            aiProfile.increaseHate();
        }
        console.log(`${aiProfile.name}: 좋아요 ${aiProfile.likecounts}, 싫어요 ${aiProfile.hatecounts}`);
      });*/
    });

  // TTS 버튼 생성
  const ttsButton = document.createElement('button');
  ttsButton.classList.add('tts-button');

  // 이미지 아이콘 추가
  const speakerIcon = new Image();
  speakerIcon.src = 'assets/images/speaker.png'; // 이미지 파일 경로

  speakerIcon.style.width = '30px'; // 이미지 가로 크기
  speakerIcon.style.height = '30px'; // 이미지 세로 크기

  ttsButton.addEventListener('click', () => {
    generateSpeech(aianswer)
    //synthesizeSpeech(aianswer)
    //play_tts(aianswer)
    //playTTS(aianswer)
        .then(() => {
            console.log('TTS 재생 완료');
        })
        .catch(error => {
            // 에러 처리
            console.error('TTS 재생 실패:', error);
        });
  });

  // 버튼에 이미지 아이콘 추가
  ttsButton.appendChild(speakerIcon);

  bottomContainer.appendChild(ttsButton);

  aiContainer.appendChild(topContainer);
  aiContainer.appendChild(bottomContainer);

  aiContainersWrapper.appendChild(aiContainer);
  });
});

