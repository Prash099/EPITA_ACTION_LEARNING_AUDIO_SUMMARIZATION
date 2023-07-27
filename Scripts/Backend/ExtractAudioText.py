import logging
from youtube_transcript_api import YouTubeTranscriptApi
from Scripts import API_URL, headers
import requests


class ExtractAudioText:
    def __init__(self):
        self.logger = logging.getLogger("logs/audio_text_extraction")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)


    def extract_audio_from_youtube(self, youtube_link):
        text = ""
        try:
            if "v=" not in youtube_link:
                video_id = youtube_link.split("/")[-1]
            else:
                video_id = youtube_link.split("v=")[1]
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            text = " ".join([line['text'] for line in transcript])
            return text
        except Exception:
            return text


    def extract_text_from_audio(self, audio_file):
        try:
            data = audio_file.read()
            response = requests.post(API_URL, headers=headers, data=data)
            # response = requests.post(API_URL_, headers=headers, data=data)
            self.logger.info("Transcript extracted successfully from the audio.")
            return response.json()['text']

        except Exception as e:
            self.logger.error(f"Failed to extract transcript from the audio. Error: {str(e)}")
            return None

