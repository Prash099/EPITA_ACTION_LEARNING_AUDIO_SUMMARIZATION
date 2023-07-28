from flask import Flask, request, jsonify
from Scripts.Backend.ExtractAudioText import ExtractAudioText
from Scripts.Backend.PassageSummarizer import PassageSummarizer
from Scripts.Backend.QASummarizer import QASummarizer
from Scripts.Backend.URLScraper import URLScraper
import logging
import os


app = Flask(__name__)

logging.basicConfig(filename='logs/audio_text_extraction.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

success_logger = logging.getLogger('success_logger')
success_logger.setLevel(logging.INFO)
success_handler = logging.FileHandler('logs/audio_text_extraction_success.log')
success_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
success_logger.addHandler(success_handler)

failure_logger = logging.getLogger('failure_logger')
failure_logger.setLevel(logging.ERROR)
failure_handler = logging.FileHandler('logs/audio_text_extraction_failure.log')
failure_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
failure_logger.addHandler(failure_handler)

audio_extractor = ExtractAudioText()
passage_summarizer = PassageSummarizer()
qa_summarizer = QASummarizer()


@app.route('/extract_audio_youtube', methods=['POST'])
def extract_audio_text_youtube():
    try:
        data = request.get_json()
        youtube_link = data.get("youtube_link")
        if youtube_link:
            text = audio_extractor.extract_audio_from_youtube(youtube_link)
            if text:
                return jsonify({"audio_transcript": text}), 200
            else:
                return jsonify({"error": "Error occurred during transcription"}), 500
        else:
            return jsonify({"error": "Invalid request payload"}), 400
    except Exception as e:
        logging.exception("Error occurred during speech-to-text API call")
        return jsonify({"error": "An unexpected error occurred"}), 500



@app.route('/')
def hello_world():
    return 'Hello from AuSUMM Flask!'

@app.route('/extract_url_text', methods=['POST'])
def extract_text_from_url():
    if not request.json or 'url' not in request.json:
        return jsonify({'error': 'Invalid request. Please provide a valid JSON payload with "url".'}), 400

    url = request.json['url']
    scraper = URLScraper()
    extracted_text = scraper.extract_text_from_website(url)

    if extracted_text:
        return jsonify({'extracted_text': extracted_text}), 200
    else:
        return jsonify({'error': 'Failed to extract text from the website.'}), 500
    

@app.route('/extract_url_text_wiki', methods=['POST'])
def extract_text_from_url_wiki():
    if not request.json or 'url' not in request.json:
        return jsonify({'error': 'Invalid request. Please provide a valid JSON payload with "url".'}), 400

    url = request.json['url']
    scraper = URLScraper()
    extracted_text = scraper.extract_text_from_wiki(url)

    if extracted_text:
        return jsonify({'extracted_text': extracted_text}), 200
    else:
        return jsonify({'error': 'Failed to extract text from the website.'}), 500
    


@app.route('/summarize_passages', methods=['POST'])
def summarize_passage_text():
    try:
        data = request.get_json()
        text = data['text']
        summary = passage_summarizer.generate_summary_passages(text)[0]['summary_text']
        if summary:
            return jsonify({"summary": summary})
        else:
            return jsonify({"error": "Failed to generate summary."}), 500
    except Exception as e:
        logging.error("Error processing PASSAGE_SUMMARIZER request: " + str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/summarize_qa', methods=['POST'])
def qa_summarize_texts():
    try:
        data = request.get_json()
        input_text = data['text']
        summary = qa_summarizer.summarize_qa_texts(input_text)[0]['generated_text']
        if summary:
            return jsonify({"summary": summary}), 200
        else:
            return jsonify({"error": "Failed to generate summary."}), 500
    except Exception as e:
        logging.error("Error processing QA_SUMMARIZER request: " + str(e))
        return jsonify({"error": "Internal server error."}), 500


@app.route('/extract_text', methods=['POST'])
def extract_text_from_audio():
        try:
            if 'audio' not in request.files:
                return jsonify({"error": "No file part"}), 400

            audio_file = request.files['audio']
            if audio_file.filename == '':
                return jsonify({"error": "No selected file"}), 400
            
            if audio_file:
                text = audio_extractor.extract_text_from_audio(audio_file)
                success_logger.info(f"Successfully extracted text from {audio_file.filename}")
                return jsonify({"text": text}), 200
            
        except Exception as e:
            failure_logger.error(f"Error in extracting text from {audio_file.filename}: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
