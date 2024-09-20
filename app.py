from flask import Flask, render_template, Response,jsonify,request
import cv2
import mediapipe as mp 
import itertools
import copy
import numpy as np 
import string 
from tensorflow import keras
import pandas as pd 
import warnings
import time 
import pyttsx3
warnings.filterwarnings("ignore")
import speech_recognition as sr
from moviepy.editor import VideoFileClip



# Load your pre-trained model
model = keras.models.load_model("model.h5", compile = False)

# Initialize MediaPipe and other variables
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Create a list of alphabets 
alphabet = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
alphabet += list(string.ascii_uppercase)

predicted_text = ""  # Initialize variable to hold the predicted text

# Function to calculate the landmark points of hands for detections
def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]
    landmark_point = []

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_point.append([landmark_x, landmark_y])

    return landmark_point

# Function to preprocess the landmark points
def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Flatten the list
    temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))
    if max_value == 0:
        return temp_landmark_list
    temp_landmark_list = [n / max_value for n in temp_landmark_list]

    return temp_landmark_list

app = Flask(__name__)
cap = cv2.VideoCapture(0)



def generate_frames():
    global predicted_text
    previous_sign = None
    start_time = None
    detection_threshold = 1

    with mp_hands.Hands(
        model_complexity=0, max_num_hands=2,
        min_detection_confidence=0.3, min_tracking_confidence=0.6
    ) as hands:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            frame = cv2.flip(frame, 1)
            image = frame.copy()
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    landmark_list = calc_landmark_list(image, hand_landmarks)
                    pre_processed_landmark_list = pre_process_landmark(landmark_list)

                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )

                    df = pd.DataFrame([pre_processed_landmark_list])
                    predictions = model.predict(df, verbose=0)
                    predicted_classes = np.argmax(predictions, axis=1)
                    label = alphabet[predicted_classes[0]]

                    cv2.putText(image, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)

                    if label == previous_sign:
                        if start_time is None:
                            start_time = time.time()
                        elif time.time() - start_time >= detection_threshold:
                            predicted_text += label
                            start_time = None
                    else:
                        previous_sign = label
                        start_time = None

            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            



def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        print("Listening for audio input...")
        audio = recognizer.record(source)
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"Recognized Text: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError:
            print("Could not request results; check your internet connection")

    return ""

def map_text_to_video(text):
    video_mapping = {
        "hello": "static/videos/hello.mp4",
        "thank": "static/videos/thank.mp4",
        "goodbye": "static/videos/goodbye.mp4",
        # Add more mappings as required
    }
    return video_mapping.get(text, None)




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/isl')
def isl_page():
    global current_model, current_labels_dict
    current_model = model
    current_labels_dict = alphabet
    return render_template('ISL.html')


@app.route('/audio_to_isl', methods=['GET', 'POST'])
def audio_to_ISL():
    if request.method == 'POST':
        # Handle file upload
        audio_file = request.files['audio']
        recognized_text = audio_to_text(audio_file)
        if recognized_text:
            video_path = map_text_to_video(recognized_text)
            if video_path:
                return jsonify({"video_path": video_path, "text": recognized_text})
            else:
                return jsonify({"error": "No matching video found for the recognized text"}), 404
        else:
            return jsonify({"error": "Could not recognize the audio"}), 400
    return render_template('audio_to_ISL.html')






@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



# Route to get the current predicted text
@app.route('/get_predicted_text', methods=['GET'])
def get_predicted_text():
    return jsonify(predicted_text=predicted_text)


@app.route('/clear_last_character', methods=['POST'])
def clear_last_character():
    global predicted_text
    if predicted_text:
        predicted_text = predicted_text[:-1]
    return jsonify(predicted_text=predicted_text)



@app.route('/speak_sentence', methods=['POST'])
def speak_sentence():
    global predicted_text
    engine = pyttsx3.init()
    engine.say(predicted_text)
    engine.runAndWait()
    return '', 204

# Route to clear the entire predicted sentence
@app.route('/clear_sentence', methods=['POST'])
def clear_sentence():
    global predicted_text
    predicted_text = ""
    return jsonify(success=True)


# Route to add a space in the predicted text
@app.route('/add_space', methods=['POST'])
def add_space():
    global predicted_text
    predicted_text += " "
    return jsonify(predicted_text=predicted_text)


if __name__ == '__main__':
    app.run(debug=True)
