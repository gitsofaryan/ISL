import speech_recognition as sr
from moviepy.editor import VideoFileClip

# Function to convert audio to text
def audio_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for audio input...")
        audio = recognizer.listen(source)
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

# Function to map text to video names and play video
def map_text_to_video(text):
    # Dictionary mapping words to video file paths
    video_mapping = {
        "hello": "videos/hello.mp4",
        "thank": "videos/thank.mp4",
        "goodbye": "videos/goodbye.mp4",
        # Add more mappings as required
    }

    if text in video_mapping:
        video_path = video_mapping[text]
        print(f"Playing video: {video_path}")
        clip = VideoFileClip(video_path)
        clip.preview()  # This will play the video using moviepy's built-in player
    else:
        print("No matching video found for the recognized text")

# Main function
def main():
    recognized_text = audio_to_text()
    if recognized_text:
        map_text_to_video(recognized_text)

if __name__ == "__main__":
    main()
