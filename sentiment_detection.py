import malaya

class Sentiment_detection:

    def __init__(self):
        self.message = ""

    def getSentiment(self, message):
        model = malaya.sentiment.multinomial()
        sentiment = model.predict(message)
        message = ' '.join(message)

        return sentiment