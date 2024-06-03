async function synthesizeSpeech(answer) {
    const text = answer;
    const apiKey = "API_KEY"; // Replace with your Elevenlabs API key
    const url = `https://api.elevenlabs.com/v1/tts?apikey=${apiKey}&text=${encodeURIComponent(text)}`;
  
    try {
      const response = await fetch(url);
      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
  
      // Create an audio element and play the synthesized audio
      const audio = new Audio(audioUrl);
      audio.play();
    } catch (error) {
      console.error("Error synthesizing speech:", error);
    }
}
export {synthesizeSpeech}
