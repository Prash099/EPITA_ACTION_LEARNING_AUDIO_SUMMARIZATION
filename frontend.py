import requests
import streamlit as st
import pandas as pd

st.set_page_config(page_title='AuSUMM', layout='wide')

def extract_text_from_website(url):
    response = requests.post("http://0.0.0.0:5000/extract_url_text", json={"url": url})
    if response.status_code == 200:
        data = response.json()
        return data.get("extracted_text")
    else:
        return None
    
def extract_text_from_wiki(url):
    response = requests.post("http://0.0.0.0:5000/extract_url_text_wiki", json={"url": url})
    if response.status_code == 200:
        data = response.json()
        return data.get("extracted_text")
    else:
        return None
    
def extract_text_from_youtube(youtube_link):
    response = requests.post("http://0.0.0.0:5000/extract_audio_youtube", json={"youtube_link": youtube_link})
    if response.status_code == 200:
        data = response.json()
        return data.get("audio_transcript")
    else:
        return None

def extract_text_from_local_audio(audio_file):
    files = {'audio': audio_file}
    response = requests.post("http://0.0.0.0:5000/extract_text", files=files)
    if response.status_code == 200:
        extracted_text = response.json().get('text')
        return extracted_text
    else:
        return "Text extraction failed. Please try again later."

def generate_summary_passages(text):
    response = requests.post("http://0.0.0.0:5000/summarize_passages", json={"text": text.lower()})
    if response.status_code == 200:
        data = response.json()
        return data.get("summary")
    else:
        return None

def generate_qa_summary(text):
    response = requests.post("http://0.0.0.0:5000/summarize_qa", json={"text": text.lower()})
    if response.status_code == 200:
        data = response.json()
        return data.get("summary")
    else:
        return None

def make_summarization():
    st.title('AuSUMM')
    st.title('Audio Summarizing!...')
    st.write('Enter your audio or video URL, upload an audio file, WebPage URL, or provide a text transcript.')
    st.write('Summarization in just a few clicks!...')

    input_option = st.selectbox('Select your input:', ['YouTube URL', 'Local Audio', 'Web URL', 'Text Transcript'])

    if input_option == 'YouTube URL':
        st.write('Select the type of Video:')
        source_option = st.radio('Source:', ['Conversational Video', 'Non Conversational Video'])
        youtube_link = st.text_input('Enter URL:', value='Your URL')
        extract_text_option = st.button('Text Extraction')
        extracted_text = st.empty()
        if extract_text_option:
            extracted_text.write('Extracted text from the YouTube URL:')
            extracted_text_input = st.text_input('', extract_text_from_youtube(youtube_link))
            st.session_state['youtube_text'] = extracted_text_input

        # if st.button('Edit'):
        #     extracted_text.write('Extracted text from the YouTube URL:')
        #     extracted_text_input = st.text_input('', st.session_state['youtube_text'])
        #     st.session_state['youtube_text'] = extracted_text_input

        if st.button('Summarize'):
            st.write('Extracted text from the YouTube URL:')
            st.write(st.session_state['youtube_text'])
            st.write('Summarized result from the YouTube URL:')
            if source_option == 'Conversational Video':
                summarized_result = generate_qa_summary(st.session_state['youtube_text'])
                if summarized_result:
                    st.write(summarized_result)
            else:
                summarized_result = generate_summary_passages(st.session_state['youtube_text'])
                if summarized_result:
                    st.write(summarized_result)

        st.experimental_set_query_params(youtube_link=youtube_link)

    elif input_option == 'Web URL':
        st.write('Select the source of the website URL:')
        source_option = st.radio('Source:', ['Wikipedia', 'Others'])
        if source_option == 'Wikipedia':
            url = st.text_input('Enter Wikipedia URL:', value='https://en.wikipedia.org/wiki/Main_Page')
        else:
            url = st.text_input('Enter URL:', value='Your URL')
        extract_text_option = st.button('Text Extraction')
        extracted_text = st.empty()
        if extract_text_option:
            if source_option == 'Wikipedia':
                extracted_text.write('Extracted text from the Wikipedia URL:')
                extracted_text_input = st.text_input('', extract_text_from_wiki(url))
                st.session_state['web_text'] = extracted_text_input
            else:
                extracted_text.write('Extracted text from the website URL:')
                extracted_text_input = st.text_input('', extract_text_from_website(url))
                st.session_state['web_text'] = extracted_text_input

        # if st.button('Edit'):
        #     if source_option == 'Wikipedia':
        #         extracted_text.write('Extracted text from the website URL:')
        #         extracted_text_input = st.text_input('', st.session_state['web_text'])
        #         st.session_state['web_text'] = extracted_text_input
        #     else:
        #         extracted_text.write('Extracted text from the website URL:')
        #         extracted_text_input = st.text_input('', st.session_state['web_text'])
        #         st.session_state['web_text'] = extracted_text_input


        if st.button('Summarize'):
            if source_option == 'Wikipedia':
                st.write('Extracted text from the Wikipedia URL:')
                st.write(st.session_state['web_text'])
                st.write('Summarized result from the website URL:')
                summarized_result = generate_summary_passages(st.session_state['web_text'])
                if summarized_result:
                    st.write(summarized_result)
            else:
                st.write('Extracted text from the website URL:')
                st.write(st.session_state['web_text'])
                st.write('Summarized result from the website URL:')
                summarized_result = generate_summary_passages(st.session_state['web_text'])
                if summarized_result:
                    st.write(summarized_result)

            st.experimental_set_query_params(url=url)

    elif input_option == 'Local Audio':
        local_audio = st.file_uploader('Upload local audio file:', type=['mp3', 'wav'])
        extract_text_option = st.button('Text Extraction')
        extracted_text = st.empty()
        if extract_text_option:
            extracted_text.write('Extracted text from local audio file:')
            extracted_text_input = st.text_input('', extract_text_from_local_audio(local_audio))
            st.session_state['audio_text'] = extracted_text_input

        # if st.button('Edit'):
        #     extracted_text.write('Extracted text from local audio file:')
        #     extracted_text_input = st.text_input('', st.session_state['audio_text'])
        #     st.session_state['audio_text'] = extracted_text_input

        if st.button('Summarize'):
            st.write('Extracted text from local audio file:')
            st.write(st.session_state['audio_text'])
            st.write('Summarized result from local audio file:')
            summarized_result = generate_qa_summary(st.session_state['audio_text'])
            if summarized_result:
                st.write(summarized_result)

        st.experimental_set_query_params(local_audio=local_audio)

    elif input_option == 'Text Transcript':
        text_transcript = st.text_area('Enter text transcript:', value='Your text transcript')

        if st.button('Summarize'):
            st.write('Input text transcript:')
            st.write(text_transcript)
            st.write('Summarized result from text transcript:')
            summarized_result = generate_summary_passages(text_transcript)
            if summarized_result:
                st.write(summarized_result)

        st.experimental_set_query_params(text_transcript=text_transcript)



nav_option = st.sidebar.selectbox('Select page:', ['Make Summarization'])

if nav_option == 'Make Summarization':
    make_summarization()

