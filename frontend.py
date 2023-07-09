import streamlit as st
from Scripts.Pages.main_page import run_main_page

def main():
    st.set_page_config(page_title="MyAudioSummarisation", page_icon=":)")
    st.title("Audio Summarization")

    with st.container():
        st.header("Description")
        st.write("##")
        st.write("""This project is a part of EPITA Master's done by Prashanth Raghavendra Rao, Vishal Muralikumar, Sela Koshy.
                    Audio Summarisation is done by extracting audio from videos, Extracting Text from audio's, preprocessing and generating summaries 
                    by training a deep learning model to extract summaries from text.""")
        # st.write("[Learn More >](https://www.kaggle.com/datasets/yasserh/wine-quality-dataset)")

    run_main_page()

if __name__ == "__main__":
    main()




# import streamlit as st
# import requests
# from Scripts.BackEnd.ExtractAudio import ExtractAudio


# def main():
#     st.set_page_config(page_title="MyAudioSummarisation", page_icon=":)")
#     st.title("Audio Summarization")
    
#     audio_extracter = ExtractAudio()

#     with st.container():
#         st.header("Description")
#         st.write("##")
#         st.write("""This project is a part of EPITA Master's done by Prashanth Raghavendra Rao, Vishal Muralikumar, Sela Koshy.
#                     Audio Summarisation is done by extracting audio from videos, Extracting Text from audio's, preprocessing and generating summaries 
#                     by training a deep learning model to extract summaries from text.""")
#         # st.write("[Learn More >](https://www.kaggle.com/datasets/yasserh/wine-quality-dataset)")

#     input_method = st.radio("Select Input Method", ("YouTube Link", "Audio File"))

#     if input_method == "YouTube Link":
#         youtube_link = st.text_input("Enter YouTube Link")
#         if st.button("Submit"):
#             if youtube_link:
#                 st.write("Extracting audio from YouTube video...")
#                 response = requests.post("http://localhost:8000/extract-audio", json={"youtube_link": youtube_link})
#                 if response.status_code == 200:
#                     st.write("Audio Text extracted successfully!")
#                     text = response.json()["text"]
#                     st.write("Text extracted from audio:")
#                     st.write(text)
#                     st.write("Summarizing...")
#                     # Make API request to generate summary
#                     summary_response = requests.post("http://localhost:8000/summarize", json={"text": text})
#                     if summary_response.status_code == 200:
#                         summary = summary_response.json()["summary"]
#                         st.write("Summary:")
#                         st.write(summary)
#                 else:
#                     st.error("Failed to extract audio from YouTube video.")
#     else:
#         audio_file = st.file_uploader("Upload Audio File", type=["wav", "mp3", "ogg"])
#         if st.button("Submit"):
#             if audio_file:
#                 st.write("Text extracted from audio:")
#                 converted_file = audio_extracter.convert_to_wav(audio_file)
#                 text = audio_extracter.extract_text_from_audio(converted_file)
#                 st.write(text)
#                 st.write("Summarizing...")
#                 # Make API request to generate summary
#                 summary_response = requests.post("http://localhost:8000/summarize", json={"text": text})
#                 if summary_response.status_code == 200:
#                     summary = summary_response.json()["summary"]
#                     st.write("Summary:")
#                     st.write(summary)


# if __name__ == "__main__":
#     main()
