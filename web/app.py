from flask import Flask, request, jsonify, send_file, render_template
from chatmodel import preprocess_image, predict_emotion, generate_first_responce, tts_function, stt_function, talk_to_gpt
from pydub import AudioSegment

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['image']
    img_bytes = file.read()
    img_array = preprocess_image(img_bytes)
    emotion = predict_emotion(img_array)
    response_text = generate_first_responce(emotion)
    tts_function(response_text)
    return send_file('output.mp3', mimetype='audio/mpeg')

@app.route('/record_audio', methods=['POST'])
def record_audio():
    audio_file = request.files['audio']
    audio_file.save('input.mp3')
    transcript = stt_function('input.mp3')
    gpt_response = talk_to_gpt(transcript)
    tts_function(gpt_response)
    return send_file('output.mp3', mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(debug=True)