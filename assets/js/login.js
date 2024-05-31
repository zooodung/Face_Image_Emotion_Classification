document.getElementById('login-button').addEventListener('click', () => {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    // 여기에 로그인 로직을 구현합니다.
    // 예: 서버에 로그인 요청을 보내거나, 입력값을 검증합니다.
  
    // 로그인 성공 시
    alert('로그인 성공!');
    window.location.href = 'main_profile.html';
  
    // 로그인 실패 시
    //alert('로그인 실패! 아이디 또는 비밀번호를 확인하세요.');
});