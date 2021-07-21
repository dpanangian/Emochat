import spacy

import json
from os.path import abspath, dirname
ROOT_PATH = dirname(dirname(abspath(__file__)))
STOP_WORD_PATH = '{}/model/stop_words.json'.format(ROOT_PATH)


class Preprocessor:

    def __init__(self):
        with open(STOP_WORD_PATH, "r") as f:
            self.stop_words = json.load(f)["words"]
        self.sp = spacy.load('de_core_news_sm')

    def preprocess_data(self, text):
        processed_text = text

        # Removal of unnecessary white spaces | Lowercasing
        processed_text = processed_text.strip().lower()
        return self.get_tokens(processed_text)

    def get_tokens(self, text):
        text_tokens = self.sp.tokenizer(text)
        string_tokens = []
        for word in text_tokens:
            if not (str(word) in self.stop_words or str(word) in ('', ' ')):
                string_tokens.append(str(word))
        return string_tokens



