from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from Scripts.BackEnd.ExtractAudio import ExtractAudio
from Scripts.BackEnd.TextSummarizer import TextSummarizer
from Scripts import SUMMARY_LENGTH

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

audio_extracter = ExtractAudio()
summarizer = TextSummarizer()

@app.post("/extract-audio")
async def extract_audio(audio_file: UploadFile = File(...)):
    converted_file = audio_extracter.convert_to_wav(audio_file.file)
    text = audio_extracter.extract_audio_text(converted_file)
    return {"audio_transcript": text}

@app.post("/summarize")
async def summarize(data: dict):
    text = data.get("text")
    if text:
        summary = summarizer.generate_summary(text, SUMMARY_LENGTH)
        return {"summary": summary}
    else:
        return {"error": "Invalid request payload"}

@app.post("/extract-audio-youtube")
async def extract_audio_youtube(data: dict):
    youtube_link = data.get("youtube_link")
    if youtube_link:
        text = audio_extracter.extract_audio_from_youtube(youtube_link)
        return {"audio_transcript": text}
    else:
        return {"error": "Invalid request payload"}
