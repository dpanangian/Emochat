from emochat.classifier.model import EmoModel


class EmoClassifier:
    # EMOTION = ['joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust', 'anger', 'anticipation']
    EMOJIS = ['😊', '🥰', '😱', '😲', '😢', '🤢', '😡', '👀']

    def __init__(self):
        self.model = EmoModel()

    def classify_emoji(self, text):
        emotion = self.model.predict_emotion(text)
        print(emotion)
        emoji = self.EMOJIS[emotion]
        return text + ' ' + emoji


if __name__ == '__main__':
    classifier = EmoClassifier()
    response = classifier.classify_emoji("Warum schießen die Italiener kein Tor?")
    print(response)


