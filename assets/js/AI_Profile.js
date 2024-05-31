// AI_Profile.js

class AI_Profile {
  constructor(name, profileimg) {
    this.name = name;         
    this.profileimg = profileimg; 
    this.likecounts = 0;
    this.hatecounts = 0;
  }

  increaseLike() {
    this.likecounts++;
  }

  increaseHate() {
    this.hatecounts++;
  }
}

// AI 이미지 생성
const ai_Anna = new AI_Profile('Anna', 'assets/images/123.png');
const ai_Kevin = new AI_Profile('Kevin', 'assets/images/ai_profile_img4.png');
const ai_Drake = new AI_Profile('Drake', 'assets/images/ai_profile_img8.png');

export { ai_Anna, ai_Kevin, ai_Drake };
