document.getElementById('login-button').addEventListener('click', async () => {
    const username = document.getElementById('username').value;
    const userintroduce = document.getElementById('introduce').value;

    console.log(username);
    console.log(userintroduce);

    if (!username) {
        alert("이름을 입력해주세요!");
        return;
    }

    let user_custom = {};

    user_custom = {
         name: username,
         introduce: userintroduce,
         emotions : []
    };

    try {
        const response = await fetch("/user_login", { 
          method: "PUT", 
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(user_custom) 
        });
    
        if (response.ok) {
            alert("생성되었습니다.");
            window.location.href = 'aisetting.html';
        } else {
            alert("저장에 실패했습니다.");
        }
    } catch (error) {
        console.error("Error saving settings:", error);
        alert("저장 중 오류가 발생했습니다.");
    }
  
    // 로그인 성공 시
    //alert('로그인 성공!');
    //window.location.href = 'aisetting.html';

    // 로그인 실패 시
    //alert('로그인 실패! 아이디 또는 비밀번호를 확인하세요.');
});