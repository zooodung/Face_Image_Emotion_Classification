import { UserProfile } from './USER_Profile.js';

document.addEventListener('DOMContentLoaded', async () => {
  let user; 

  try {
    const response = await fetch('http://127.0.0.1:8000/user'); 
    if (response.ok) {
      const userData = await response.json();
      user = new UserProfile(userData.name, userData.introduce);
      user.emotions = userData.emotions;
    } else {
      console.error("서버에서 사용자 데이터를 가져오는데 실패했습니다.");
    }
  } catch (error) {
    console.error("오류 발생:", error);
  }

  if (user) {
    document.getElementById('user-name').textContent = user.name;
    document.getElementById('user-introduce').textContent = user.introduce;

    const emotionCounts = { happy: 0, anger: 0, panic: 0, sad: 0 };
    user.emotions.forEach(emotion => emotionCounts[emotion.emotion]++);

    document.querySelector('.emotion-item1 .emotion-count').textContent = emotionCounts.happy;
    document.querySelector('.emotion-item2 .emotion-count').textContent = emotionCounts.anger;
    document.querySelector('.emotion-item3 .emotion-count').textContent = emotionCounts.panic;
    document.querySelector('.emotion-item4 .emotion-count').textContent = emotionCounts.sad;
  }

  const fixProfileButton = document.getElementById("fix-profile-btn");
  fixProfileButton.addEventListener("click", function() {
    window.location.href = "fix_profile.html";
  });

  const newPostButton = document.querySelector('.new-post-button');
  newPostButton.addEventListener('click', () => {
    window.location.href = 'make_log.html'; 
  });

  const aisettingButton = document.querySelector('.aisetting-button');
  aisettingButton.addEventListener('click', () => {
    window.location.href = 'aisetting.html'; 
  });

  const chatButton = document.querySelector('.chat-button');
  chatButton.addEventListener('click', function() {
    window.location.href = 'ai_chat.html';
  });

  const monthButtons = {
    'btn-jan': 1, 'btn-feb': 2, 'btn-mar': 3, 'btn-apr': 4, 'btn-may': 5,
    'btn-jun': 6, 'btn-jul': 7, 'btn-aug': 8, 'btn-sep': 9, 'btn-oct': 10,
    'btn-nov': 11, 'btn-dec': 12,
  };

  for (const buttonId in monthButtons) {
    const button = document.getElementById(buttonId);
    const month = monthButtons[buttonId];

    button.addEventListener('click', () => {
      const dailyEmotionsContainer = document.querySelector('.daily-emotions-container');
      dailyEmotionsContainer.innerHTML = '';

      const monthEmotions = user ? user.emotions.filter(emotion => emotion.month === month) : [];

      if (monthEmotions.length > 0) {
        monthEmotions.forEach(emotion => {
          const imageButton = document.createElement('button');
          imageButton.classList.add('daily-emotion-button');

          const dateSpan = document.createElement('span');
          dateSpan.textContent = `${emotion.date}`;
          dateSpan.classList.add('daily-emotion-date');
          imageButton.appendChild(dateSpan);

          const squareDiv = document.createElement('div');

          if (emotion.imageUrl) {
            const img = document.createElement('img');
            img.src = emotion.imageUrl;
            img.alt = `${emotion.emotion} 이미지`;
            img.style.maxWidth = '100%'; 
        
            // 이미지 로드 완료 후 squareDiv에 추가
            img.onload = () => {
              squareDiv.appendChild(img);
            };
        
            // 이미지 로드 실패 시 오류 처리
            img.onerror = () => {
              console.error("이미지 로드 실패:", emotion.imageUrl);
            };
          } else {
            // imageUrl이 없는 경우 기존 동작 유지
            console.error("이미지 로드 실패:", emotion.imageUrl);
            squareDiv.classList.add('daily-emotion-square');
          }

          imageButton.appendChild(squareDiv);

          const emotionSpan = document.createElement('span');
          emotionSpan.textContent = emotion.emotion;
          emotionSpan.classList.add('daily-emotion-emotion');

          if (emotion.emotion === 'happy') {
            emotionSpan.style.color = 'rgba(247, 243, 2, 0.747)';
          } else if (emotion.emotion === 'anger') {
            emotionSpan.style.color = 'rgba(228, 91, 91, 0.801)';
          } else if (emotion.emotion === 'panic') {
            emotionSpan.style.color = 'rgb(77, 158, 97)';
          } else if (emotion.emotion === 'sad') {
            emotionSpan.style.color = 'rgb(99, 150, 226)';
          }

          imageButton.appendChild(emotionSpan);

          imageButton.addEventListener('click', () => {
            const text = emotion.text;
            const emotionValue = emotion.emotion; // 감정 값을 emotionValue 변수에 저장
            const date = emotion.date;
            const year = emotion.year;
            const month = emotion.month;
            const aianswer = emotion.aianswer;
            const aicharacter = emotion.aicharacter;
            const imagepath = emotion.imageUrl;

            const params = new URLSearchParams({
              text,
              date, // 수정된 date 값
              emotion: emotionValue, // emotionValue 사용
              year,
              month,
              aianswer,
              aicharacter,
              imagepath
            });

            console.log("클릭된 이미지의 데이터:");
            console.log("Date:", emotion.date);
            console.log("Emotion:", emotion.emotion);
            console.log("Text:", emotion.text);
            console.log("Year:", emotion.year);
            console.log("Month:", emotion.month);
            console.log("AI Answer:", emotion.aianswer);
            console.log("AI Character:", emotion.aicharacter);
            console.log("Image URL:", emotion.imageUrl);
            window.location.href = `detail_log.html?${params.toString()}`;
          });

          dailyEmotionsContainer.appendChild(imageButton);
        });
      } else {
        const noDataMessage = document.createElement('p');
        noDataMessage.textContent = '데이터가 없음';
        dailyEmotionsContainer.appendChild(noDataMessage);
      }
    });
  }
});