MODEL_QA_NAME = "models/"
SEGMENT_SIZE = 10
MODEL_PASSAGES_NAME="cs608/billsum-full-data"

#Speech2Text
API_URL = "https://api-inference.huggingface.co/models/zuu/automatic-speech-recognition"
# API_URL_ = "https://api-inference.huggingface.co/models/facebook/wav2vec2-base-960h"
#Summarize
API_URL_PASSAGE = "https://api-inference.huggingface.co/models/cs608/billsum-full-data"
API_URL_QA = "https://api-inference.huggingface.co/models/jaynlp/t5-large-samsum"
API_URL_QA_ = "https://api-inference.huggingface.co/models/Prashanth2499/T5_Samsum"

#Creds
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}
