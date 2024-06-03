import { UserProfile } from './USER_Profile.js';

document.getElementById('login-button').addEventListener('click', async () => {
  let user;
  let userData;

  try {
    const response = await fetch('http://127.0.0.1:8000/user');
    if (response.ok) {
      userData = await response.json();
      user = new UserProfile(userData.name, userData.introduce);
      user.emotions = userData.emotions;
    } else {
      console.error("서버에서 사용자 데이터를 가져오는데 실패했습니다.");
    }
  } catch (error) {
    console.error("오류 발생:", error);
  }

  const username = document.getElementById('username').value;
  const userintroduce = document.getElementById('introduce').value;
    
  console.log(username);
  console.log(userintroduce);

  if (!username) {
      alert("이름을 입력해주세요!");
      return;
  }

  let user_custom = {};

  if (userData) {
    user_custom = {
      name: username,
      introduce: userintroduce,
      emotions: userData.emotions
    };

    try {
      const response = await fetch("/user_login", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user_custom)
      });

      if (response.ok) {
        alert("수정되었습니다.");
        window.location.href = 'main_profile.html';
      } else {
        alert("수정에 실패했습니다.");
      }
    } catch (error) {
      console.error("Error saving settings:", error);
      alert("저장 중 오류가 발생했습니다.");
    }
  } else {
    alert("사용자 데이터를 가져오는 데 실패했습니다.");
  }
});
