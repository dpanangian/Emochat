from emochat.classifier.model import EmoModel
from emochat.classifier.preprocessor import Preprocessor


class EmoClassifier:
    # EMOTION = ['joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust', 'anger', 'anticipation']
    EMOJIS = ['😊', '🥰', '😱', '😲', '😢', '🤢', '😡', '👀']

    def __init__(self):
        self.model = EmoModel()
        self.preprocessor = Preprocessor()

    def classify_emoji(self, text):
        preprocessed_text = self.preprocessor.preprocess_data(text)
        print(preprocessed_text)
        emotion, probability = self.model.predict_emotion(preprocessed_text)
        print(emotion, probability)
        percentage = int(probability * 100)
        emoji = self.EMOJIS[emotion]
        return text + ' ' + emoji + ' (' + str(percentage) + '%)'


if __name__ == '__main__':
    classifier = EmoClassifier()
    response = classifier.classify_emoji("Ich hatte heute eine echt spannende Sitzung")
    print(response)


