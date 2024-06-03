document.querySelector('.save-button').addEventListener('click', async () => {
  let userSettings = {};

  const attitudeChecked = document.querySelector('input[name="attitude"]:checked');
  const intensityChecked = document.querySelector('input[name="intensity"]:checked');
  const lengthChecked = document.querySelector('input[name="length"]:checked');

  const emptyFields = [];  
  if (!attitudeChecked) {
    emptyFields.push("대화 태도");
  }

  if (!intensityChecked) {
    emptyFields.push("답변 강도");
  }

  if (!lengthChecked) {
    emptyFields.push("답변 길이");
  }

  if (emptyFields.length > 0) {
    if(emptyFields.length == 1) alert(emptyFields + "를 선택해주세요!");
    else alert(emptyFields.join(", ") + "를 모두 선택해주세요!");

    return;
  }



  userSettings.a_attitude = attitudeChecked.value;
  userSettings.intensity = parseFloat(intensityChecked.value); 
  userSettings.length = parseInt(lengthChecked.value, 10); 

  const selectedCompositions = [];
  document.querySelectorAll('input[name="composition"]:checked').forEach(checkbox => {
      selectedCompositions.push(checkbox.value);
  });
  userSettings.composition = selectedCompositions.length === 0 ? ["공감하기", "위로하기", "조언하기"] : selectedCompositions;

  console.log("대화 태도: ", userSettings.a_attitude);
  console.log("답변 구성: ", userSettings.composition);
  console.log("답변 강도: ", userSettings.intensity);
  console.log("답변 길이: ", userSettings.length);

  try {
      const response = await fetch("/user_settings", { 
        method: "PUT", 
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userSettings) 
      });
  
      if (response.ok) {
          alert("저장되었습니다.");
          window.location.href = 'main_profile.html';
      } else {
          alert("저장에 실패했습니다.");
      }
  } catch (error) {
      console.error("Error saving settings:", error);
      alert("저장 중 오류가 발생했습니다.");
  }
});
