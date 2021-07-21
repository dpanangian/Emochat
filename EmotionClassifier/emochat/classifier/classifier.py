from emochat.classifier.model import EmoModel
from emochat.classifier.preprocessor import Preprocessor
from emochat.classifier.util import load_model, load_dataframe, tokenize_filter, SVM_MODEL, LR_MODEL
import logging
logging.basicConfig()
logging.root.setLevel(logging.INFO)
EMOJIS_map = {'joy':'😊','trust': '🥰','fear':'😱', 'surprise':'😲','sadness': '😢','disgust': '🤢', 'anger':'😡', 'anticipation':'👀'}


class EmoClassifier:

    def __init__(self):
        self.model = EmoModel()
        self.preprocessor = Preprocessor()

    def classify_emoji(self, text, context):
        logging.info(f"Full context: {context}")
        preprocessed_context = []
        for item in context:
            if any(emoji in item for emoji in list(EMOJIS_map.values())):
                item_without_emoji = item[:-8]  # take message without emoji
                preprocessed_context += self.preprocessor.preprocess_data(item_without_emoji)
            else:
                preprocessed_context += self.preprocessor.preprocess_data(item)
        logging.info(f"Preprocessed context {preprocessed_context}")
        preprocessed_text = self.preprocessor.preprocess_data(text)
        logging.info(f"Preprocessed message {preprocessed_text}")
        emotion, probability = self.model.predict_emotion(preprocessed_context + preprocessed_text)
        logging.info(f"Emotion index: {emotion} with probability: {probability}")
        percentage = int(probability * 100)
        emoji = list(EMOJIS_map.values())[emotion]
        return text + ' ' + emoji + ' (' + str(percentage) + '%)'


class ScikitClassifier():
    def __init__(self,path):
        self.model = load_model(path)

    def classify_emoji(self, texts, n_window=4):
        input = texts[-n_window:]
        if len(input) < n_window:
            input= ([''] * (n_window-len(input))) + input
        dict_input = [{f"utterance-{i+1}":input[-(1+i)]for i in range(4)}]
        df_input = load_dataframe(dict_input) 
        emotion = self.model.predict(df_input)[0]
        emoji = EMOJIS_map[emotion]
        output = input[-1] + " " +emoji
        return output



class SvmClassifier(ScikitClassifier):
    def __init__(self):
        super(SvmClassifier,self).__init__(SVM_MODEL)

    def classify_emoji(self, texts):
        super(SvmClassifier,self).classify_emoji(texts)

class LrClassifier(ScikitClassifier):
    def __init__(self):
        super(LrClassifier,self).__init__(LR_MODEL)

    def classify_emoji(self, texts):
        super(LrClassifier,self).classify_emoji(texts)


if __name__ == '__main__':
    classifier = EmoClassifier()
    response = classifier.classify_emoji("Das war bestimmt Absicht", context=["Du hast mein Auto kaputt gemacht"])
    print(response)


