from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import numpy as np
import json
from os.path import abspath, dirname, isfile
ROOT_PATH = dirname(dirname(abspath(__file__)))
WORDS_PATH = '{}/model/words.json'.format(ROOT_PATH)
URL = "https://drive.google.com/file/d/1jr5kzcDq6OSHYwF_rQMD9P1UFv7_SbZ3/view?usp=sharing"
MODEL_PATH = '{}/model/model.h5'.format(ROOT_PATH)
if not isfile(MODEL_PATH):
    from zipfile import ZipFile
    ZIP_PATH = '{}/model/model.zip'.format(ROOT_PATH)
    with ZipFile(ZIP_PATH, 'r') as zipObj:
        zipObj.extractall('{}/model'.format(ROOT_PATH))


class EmoModel:
    MAX_NB_WORDS = 50000
    MAX_SEQUENCE_LENGTH = 250

    def __init__(self):
        self.model = load_model(MODEL_PATH)
        self.tokenizer = Tokenizer(num_words=self.MAX_NB_WORDS, split=' ', oov_token='<unw>',
                                   filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~\'')

        with open(WORDS_PATH, 'r') as f:
            self.vocabulary = json.load(f)
        self.tokenizer.fit_on_texts(self.vocabulary)

    def predict_emotion(self, text):
        sequence = self.tokenizer.texts_to_sequences([text])
        sequence = pad_sequences(sequence, maxlen=self.MAX_SEQUENCE_LENGTH)
        probabilities = self.model.predict(sequence)
        prediction = np.argmax(probabilities)
        return prediction


