import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


class TextSummarizer:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def preprocess_text(self, text):
        doc = self.nlp(text)
        tokens = [token.text for token in doc]
        return tokens

    def calculate_word_frequencies(self, tokens):
        word_frequencies = {}

        for word in tokens:
            if self._is_valid_word(word):
                if word not in word_frequencies:
                    word_frequencies[word] = 0
                word_frequencies[word] += 1

        max_frequency = max(word_frequencies.values())
        word_frequencies = {word: frequency / max_frequency for word, frequency in word_frequencies.items()}

        return word_frequencies

    def _is_valid_word(self, word):
        return word.lower() not in STOP_WORDS and word.lower() not in punctuation

    def calculate_sentence_scores(self, text, word_frequencies):
        doc = self.nlp(text)
        sentence_scores = {}

        for sent in doc.sents:
            sentence_scores[sent] = sum(word_frequencies.get(word.text.lower(), 0) for word in sent)

        return sentence_scores

    def select_top_sentences(self, sentence_scores, select_length):
        return nlargest(select_length, sentence_scores, key=sentence_scores.get)
    
    def generate_summary(self, text, percentage):
        tokens = self.preprocess_text(text)
        word_frequencies = self.calculate_word_frequencies(tokens)
        sentence_scores = self.calculate_sentence_scores(text, word_frequencies)

        select_length = int(len(sentence_scores) * percentage)
        summary_sentences = self.select_top_sentences(sentence_scores, select_length)
        summary = [sent.text for sent in summary_sentences]

        return ' '.join(summary)