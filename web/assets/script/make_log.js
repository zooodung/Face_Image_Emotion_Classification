// go to main
function handleFormSubmit(event) {
    event.preventDefault(); // 기본 제출 행위를 막습니다.
    const form = document.getElementById('dataForm');
    const formData = new FormData(form);

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // 데이터 저장 성공 메시지를 보여주고 페이지를 리다이렉트합니다.
        const year = formData.get('year');
        const month = formData.get('month').padStart(2, '0'); // 항상 두 자리 숫자를 유지
        const date = formData.get('date').padStart(2, '0'); // 항상 두 자리 숫자를 유지
        alert(`${year}년 ${month}월 ${date}일의 일기를 저장했습니다.`);
        // setTimeout(() => {
        //     window.location.href = './main.html'; // 2초 후 main.html로 리다이렉트
        // }, 2000);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('저장에 실패했습니다.');
    });
}


// make date
function getTodayKST() {
    var now = new Date();
    var utc = now.getTime() + (now.getTimezoneOffset() * 60000);
    var kstOffset = 9; // UTC+9
    return new Date(utc + (3600000 * kstOffset));
}

function setDefaultDate() {
    var today = getTodayKST();
    document.getElementById('year').value = today.getFullYear();
    document.getElementById('month').value = today.getMonth() + 1; // getMonth()는 0부터 시작하므로 1을 더함
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
        document.getElementById('year').value = today.getFullYear(); // Reset to this year
    }

    if (month < 1 || month > 12) {
        alert('1월에서 12월 사이의 값을 입력해 주세요.');
        document.getElementById('month').value = today.getMonth(); // Reset to this month
    }

    if (parseInt(dateInput.value) > maxDate) {
        alert('선택하신 날짜가 유효하지 않습니다. 올바른 날짜를 선택해 주세요.');
        document.getElementById('year').value = today.getFullYear(); // Reset to this year
        document.getElementById('month').value = today.getMonth(); // Reset to this month
        document.getElementById('date').value = today.getDate(); // Reset to this mont
    }

    if (!year || !month || !date) {
        alert('입력되지 않은 날짜가 있습니다. 날짜를 확인해주세요.');
        document.getElementById('year').value = today.getFullYear(); // Reset to this year
        document.getElementById('month').value = today.getMonth(); // Reset to this month
        document.getElementById('date').value = today.getDate(); // Reset to this month
    }
    
    const inputDate = new Date(year, month - 1, date);
    const today = new Date(); // 현재 날짜를 가져옵니다.
    today.setHours(0, 0, 0, 0); // 시간, 분, 초, 밀리초를 0으로 설정하여 정확한 날짜 비교를 할 수 있도록 합니다.


    // 년도와 월이 미래인지 검사
    const currentYear = today.getFullYear();
    const currentMonth = today.getMonth() + 1; // getMonth()는 0부터 시작하므로 +1

    if (year > currentYear || (year === currentYear && month > currentMonth)) {
        alert('미래의 년도나 월을 선택할 수 없습니다.');
        document.getElementById('year').value = currentYear;
        document.getElementById('month').value = currentMonth;
        dateInput.value = today.getDate();
    } else if (inputDate > today) {
        // 선택한 날짜가 미래인지 검사
        alert('미래 날짜를 선택할 수 없습니다.');
        dateInput.value = today.getDate();
    }

    // if (textInput == "" || textInput == null || textInput == undefined || ( textInput != null && typeof textInput == "object" && !Object.keys(textInput).length)) {
    //     alert('일기 내용이 입력되지 않았습니다. 다시한번 확인해주세요.');
    // }
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

window.onload = function() {
    setDefaultDate(); // 페이지 로드 시 기본 날짜 설정
    updateDateConstraints(); // 초기 페이지 로드 시 날짜 제약 조건을 업데이트합니다.
} 
// make log
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