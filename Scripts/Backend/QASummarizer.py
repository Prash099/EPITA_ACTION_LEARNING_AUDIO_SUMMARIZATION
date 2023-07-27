import json
import logging
from Scripts import API_URL_QA, headers
import requests

class QASummarizer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.success_logger = logging.getLogger('QA_SuccessLogger')
        self.success_logger.setLevel(logging.INFO)
        success_handler = logging.FileHandler('logs/QA_success_log.txt')
        success_handler.setFormatter(formatter)
        self.success_logger.addHandler(success_handler)

        self.failure_logger = logging.getLogger('QA_FailureLogger')
        self.failure_logger.setLevel(logging.INFO)
        failure_handler = logging.FileHandler('logs/QA_failure_log.txt')
        failure_handler.setFormatter(formatter)
        self.failure_logger.addHandler(failure_handler)



    def summarize_qa_texts(self, text):
        try:
            data = json.dumps(text)
            summary = requests.request("POST", API_URL_QA, headers=headers, data=data)
            self.logger.info(f"SUCCESS: Summary: {summary}")
            return json.loads(summary.content.decode("utf-8"))
        except Exception as e:
            self.logger.error(f"FAILURE: Error occurred during summarization: {str(e)}")
            return None