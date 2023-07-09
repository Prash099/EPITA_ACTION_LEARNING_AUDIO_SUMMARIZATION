import streamlit as st
import requests

def run_main_page():
    input_method = st.radio("Select Input Method", ("YouTube Link", "Audio File"))

    if input_method == "YouTube Link":
        youtube_link = st.text_input("Enter YouTube Link")
        if st.button("Submit"):
            if youtube_link:
                st.write("Extracting audio from YouTube video...")
                response = requests.post("http://localhost:8000/extract-audio-youtube", json={"youtube_link": youtube_link})

                if response.status_code == 200:
                    st.write("Audio Text extracted successfully!")
                    text = response.json()["audio_transcript"]
                    st.write("Text extracted from audio:")
                    st.write(text)

                    st.write("Summarizing...")
                    summary_response = requests.post("http://localhost:8000/summarize", json={"text": text})
                    if summary_response.status_code == 200:
                        summary = summary_response.json()["summary"]
                        st.write("Summary:")
                        st.write(summary)
                else:
                    st.error("Failed to extract audio from YouTube video.")
    else:
        audio_file = st.file_uploader("Upload Audio File", type=["wav", "mp3", "ogg"])
        if st.button("Submit"):
            if audio_file:
                st.write("Text extracted from audio:")
                response = requests.post("http://localhost:8000/extract-audio", files={"audio_file": audio_file})

                if response.status_code == 200:
                    st.write("Audio Text extracted successfully!")
                    text = response.json()["audio_transcript"]
                    st.write("Text extracted from audio:")
                    st.write(text)

                    st.write("Summarizing...")
                    summary_response = requests.post("http://localhost:8000/summarize", json={"text": text})
                    if summary_response.status_code == 200:
                        summary = summary_response.json()["summary"]
                        st.write("Summary:")
                        st.write(summary)
                else:
                    st.error("Failed to extract audio from Audio File.")

