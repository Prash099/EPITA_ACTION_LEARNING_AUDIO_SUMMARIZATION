import logging
import torch
from transformers import AutoTokenizer, T5ForConditionalGeneration
from Scripts import MODEL_QA_NAME

class QASummarizer:
    def __init__(self, max_len_text=300, max_len_summary=70):
        self.model_dir = MODEL_QA_NAME
        self.max_len_text = max_len_text
        self.max_len_summary = max_len_summary
        self.tokenizer = AutoTokenizer.from_pretrained('t5-base', model_max_length=self.max_len_text)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_dir)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


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

    def _generate_summary(self, input_text):
        with torch.no_grad():
            tokenized_text = self.tokenizer(input_text, truncation=True, padding=True, return_tensors='pt')
            source_ids = tokenized_text['input_ids'].to(self.device, dtype=torch.long)
            source_mask = tokenized_text['attention_mask'].to(self.device, dtype=torch.long)

            generated_ids = self.model.generate(
                input_ids=source_ids,
                attention_mask=source_mask,
                max_length=self.max_len_summary,
                num_beams=5,
                repetition_penalty=1,
                length_penalty=1,
                early_stopping=True,
                no_repeat_ngram_size=2
            )

            summary = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
            return summary

    def summarize_qa_texts(self, input_text):
        try:
            summary = self._generate_summary(input_text)
            self.logger.info("Summary generated successfully.")
            self.success_logger.info(input_text + "\n" + summary + "\n")
            return summary
        except Exception as e:
            self.logger.error("Failed to generate summary.")
            self.failure_logger.error(input_text + "\n" + str(e) + "\n")
            return None
