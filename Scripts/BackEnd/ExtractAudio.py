import speech_recognition as sr
from pydub import AudioSegment
import tempfile
from youtube_transcript_api import YouTubeTranscriptApi

class ExtractAudio:
    def __init__(self) -> None:
        pass

    def convert_to_wav(self, audio_file):
        audio = AudioSegment.from_file(audio_file)
        wav_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        audio.export(wav_file.name, format="wav")
        return wav_file.name

    def extract_text_from_audio(self, audio_file):
        r = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
        return text

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

    def extract_audio_text(self, audio_file):
        r = sr.Recognizer()
        segment_duration = 10

        with sr.AudioFile(audio_file) as source:
            audio = r.record(source, duration=segment_duration)

        text_transcriptions = []
        while audio:
            try:
                text = r.recognize_google(audio)
                text_transcriptions.append(text)
                audio = r.record(source, duration=segment_duration, offset=len(audio))
            except sr.UnknownValueError:
                print("Error: Failed to transcribe segment.")
                audio = r.record(source, duration=segment_duration, offset=len(audio))
            except sr.RequestError as e:
                print(f"Error: {e}")
                break

        complete_text = " ".join(text_transcriptions)
        return complete_text
