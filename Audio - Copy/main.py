from flask import Flask, render_template, request, jsonify
from moviepy.editor import ImageSequenceClip
import os

app = Flask(__name__)

# Function to convert characters to video
def character_to_video(text):
    image_folder = 'static/images'
    images = []
    
    for char in text:
        image_path = os.path.join(image_folder, f"{char}.jpg")
        if os.path.exists(image_path):
            images.append(image_path)
        else:
            print(f"No image found for character: {char}")
    
    if images:
        video_path = os.path.join('static/videos', 'char_video.mp4')
        clip = ImageSequenceClip(images, fps=1)  # Adjust FPS as needed
        clip.write_videofile(video_path, codec='libx264')
        return video_path
    
    return None

# Function to map text to gesture-level video paths
def gesture_to_video(text):
    video_mapping = {
        "hello": "static/videos/hello.webm",
        "thank you": "static/videos/thank.mp4",
        "goodbye": "static/videos/goodbye.webm",
        "thanks": "static/videos/thank.mp4",
        "how are you":"static/videos/how are you.webm",
        "niceday":"static/videos/niceday.webm",
        "excuse":"static/videos/excuse.webm",
        "delivery":"static/videos/delivery.webm",
        "direction":"static/videos/direction.webm"
        # Add more mappings as required
    }
    
    return video_mapping.get(text.lower(), None)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    text = request.json.get('text', '')
    level = request.json.get('level', '')

    if level == "character":
        video_path = character_to_video(text.lower())
    elif level == "gesture":
        video_path = gesture_to_video(text.lower())
    else:
        return jsonify({"error": "Invalid conversion level"}), 400
    
    if video_path:
        return jsonify({"video_path": video_path})
    else:
        return jsonify({"error": "No matching video or images found for the given text"}), 404

if __name__ == "__main__":
    app.run(debug=True,port=1000)
