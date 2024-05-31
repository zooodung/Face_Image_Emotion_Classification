class UserProfile {
    constructor(name, introduce) {
      this.name = name;
      this.introduce = introduce;
      this.emotions = [];
    }
  
    addEmotion(emotion) {
      this.emotions.push(emotion);
    }
  }
  
  class UserEmotion {
    constructor(year, month, date, text, emotion, aicharacter, imageUrl = null, aianswer) { // imageUrl 속성 추가
      this.year = year;
      this.month = month;
      this.date = date;
      this.text = text;
      this.emotion = emotion;
      this.aicharacter = aicharacter; // aicharacter 속성 추가
      this.aianswer = aianswer;
      this.imageUrl = imageUrl; // imageUrl 속성 추가 및 기본값 null 설정
    }
  }
  
  
  class LLManswer {
    constructor(name, answer) {
      this.name = name;
      this.answer = answer;
    }
  }
  
  // 초기 데이터는 더 이상 필요하지 않음 (서버에서 관리)
  // const user = new UserProfile("홍길동", "I'm Hong Kildong"); // user 객체는 서버에서 가져옴
  
  export { UserProfile, UserEmotion };
  