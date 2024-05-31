import { UserEmotion, UserProfile } from './USER_Profile.js';

document.querySelector('.confirm-btn').addEventListener('click', async function (event) {
  if (!validateForm()) {
    event.preventDefault();
    return;
  }

  const form = document.getElementById('dataForm');
  const year = form.year.value;
  const month = ('0' + form.month.value).slice(-2);
  const date = ('0' + form.date.value).slice(-2);
  const textInput = form.textInput.value;
  const imageInput = form.imageInput.files[0];

  let imageUrl = null;
  let emotion = null;
  let aianswer = null;
  //let predictedEmotion = null;

  const formData = new FormData();

  if (imageInput) {
    document.getElementById('loadingOverlay').style.display = 'flex';

    formData.append('image', imageInput);
    
    try {
      const response = await fetch('http://127.0.0.1:8000/upload_image', {
        method: 'POST',
        body: formData
        
      });
      
      if (response.ok) {
        const data = await response.json(); 
        imageUrl = data.imageUrl;
        
        if (data.emotion == 'sadness')
          emotion = 'sad';
        else {
          emotion = data.emotion; 
        }
  
        console.log("이미지가 서버에 성공적으로 업로드되었습니다.", imageUrl, "Emotion: ", emotion); 
      } else {
        console.error("이미지 업로드 실패:", response.statusText);
      }
    } catch (error) {
      console.error("이미지 업로드 오류:", error);
      document.getElementById('loadingOverlay').style.display = 'none';
    
      await showErrorAndResetForm().then(() => {
        location.reload();
      });

      return;
    }
  }

/*
  try {
    const filename = imageUrl.replace('/images/', '');
    console.log("filename = ", filename);
  
    const response = await fetch(`http://127.0.0.1:8000/predict_emotion?filename=${filename}`);
  
    if (response.ok) {
      const data = await response.json();
      predictedEmotion = data.emotion;
      console.log("감정 분석 결과:", predictedEmotion);
    } else {
      console.error("감정 분석 실패:", response.statusText);
    }
  } catch (error) {
    console.error("감정 분석 오류:", error);
  }
*/
  aianswer = await get_aiAnswer(emotion, textInput)

  try {
    const response = await fetch('/user', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (response.ok) {
      const userData = await response.json();
      const user = new UserProfile(userData.name, userData.introduce);
      user.emotions = userData.emotions;
      
      const newEmotion = new UserEmotion(
        parseInt(year), parseInt(month), parseInt(date), textInput, emotion, "Anna", imageUrl, aianswer
      );
  
      user.addEmotion(newEmotion); // user 객체에 새로운 감정 추가
  
      const updateResponse = await fetch('/user', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        
        body: JSON.stringify(user) // user 객체 전체를 전송
      });

      if (updateResponse.ok) {
        console.log("사용자 데이터가 서버에 성공적으로 업데이트 되었습니다.");
        document.getElementById('loadingOverlay').style.display = 'none';
        console.log("Year:", year);
        console.log("Month:", month);
        console.log("Date:", date);
        console.log("Text Input:", textInput);
        console.log("ImageURL:", imageUrl); // 이미지 파일 출력
        //console.log("predictedEmotion: ", predictedEmotion)
        console.log("Emotion: ", emotion)
        console.log("AI answer: ", aianswer)
        
        window.location.href = 'main_profile.html';
      } else {
        console.error("서버에 사용자 데이터를 업데이트하는데 실패했습니다.");
      }
    } else {
      console.error("서버에서 사용자 데이터를 가져오는데 실패했습니다.");
    }
  } catch (error) {
    console.error("오류 발생:", error);
  }
});

window.onload = setDefaultDate;

function getTodayKST() {
    var now = new Date();
    var utc = now.getTime() + (now.getTimezoneOffset() * 60000);
    var kstOffset = 9;
    return new Date(utc + (3600000 * kstOffset));
}

var today = getTodayKST();

function setDefaultDate() {
    document.getElementById('year').value = today.getFullYear();
    document.getElementById('month').value = today.getMonth() + 1;
    document.getElementById('date').value = today.getDate();
    updateDateConstraints();
}

function daysInMonth(year, month) {
    return new Date(year, month, 0).getDate();
}

function updateDateConstraints() {
    var year = parseInt(document.getElementById('year').value);
    var month = parseInt(document.getElementById('month').value);
    var dateInput = document.getElementById('date');
    var maxDate = daysInMonth(year, month);
    dateInput.max = maxDate;

    if (year < 2000 || year > 2100) {
        alert('2000년도부터 2100년도 사이의 값을 입력해 주세요.');
        document.getElementById('year').value = today.getFullYear();
    }

    if (month < 1 || month > 12) {
        alert('1월에서 12월 사이의 값을 입력해 주세요.');
        document.getElementById('month').value = today.getMonth();
    }

    if (parseInt(dateInput.value) > maxDate) {
        alert('선택하신 날짜가 유효하지 않습니다. 올바른 날짜를 선택해 주세요.');
        dateInput.value = today.getDate();
    }
}

function validateForm() {
  const form = document.getElementById('dataForm');
  const year = form.year.value;
  const month = form.month.value;
  const date = form.date.value;
  const textInput = form.textInput.value;

  // 필수 필드 검사
  if (!year || !month || !date || !textInput) {
    alert('모든 필드를 입력해주세요.');
    return false;
  }

  // 날짜 유효성 검사 (예시)
  const inputDate = new Date(year, month - 1, date);
  const today = new Date();
  if (inputDate > today) {
    alert('미래 날짜를 선택할 수 없습니다.');
    return false;
  }

  return true; // 모든 검사 통과
}

document.getElementById('year').addEventListener('change', updateDateConstraints);
document.getElementById('month').addEventListener('change', updateDateConstraints);
document.getElementById('date').addEventListener('change', function() {
    var year = parseInt(document.getElementById('year').value);
    var month = parseInt(document.getElementById('month').value);
    var date = parseInt(document.getElementById('date').value);
    var maxDate = daysInMonth(year, month);

    if (date > maxDate) {
        alert('선택하신 날짜가 유효하지 않습니다. 올바른 날짜를 선택해 주세요.');
        document.getElementById('date').value = maxDate;
    }
});


document.querySelector('.upload-btn').addEventListener('change', function(event) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const imgElement = document.createElement('img');
        imgElement.src = e.target.result;  
        imgElement.style.maxWidth = "100%"; // 이미지 크기 조절 (필요에 따라 조정)

        document.querySelector('.image-upload').innerHTML = ''; // 기존 내용 삭제
        document.querySelector('.image-upload').appendChild(imgElement); // 이미지 추가
    };
    reader.readAsDataURL(event.target.files[0]);
});

async function showErrorAndResetForm() {
  document.getElementById('errorOverlay').style.display = 'flex';
  return new Promise(resolve => { 
    setTimeout(() => {
      document.getElementById('errorOverlay').style.display = 'none';
      resolve(); // 3초 후에 Promise를 resolve
    }, 2500);
  });
}

async function get_aiAnswer(user_emotion, user_text) {
  const requestData = {
    text: String(user_text),
    emotion: String(user_emotion)
  };

  const response = await fetch('/generate_response', { 
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
  });

  if (response.ok) {
      const data = await response.json();
      return data.response; 
  } else {
      throw new Error('AI 답변 생성 실패');
  }
}
