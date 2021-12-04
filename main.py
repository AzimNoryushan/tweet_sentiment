from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from topic_sentiment import Topic_sentiment
import json

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
model = Topic_sentiment()

@app.route("/")
@cross_origin()
def main_page():
    return render_template('index.html')    

@app.route("/topic", methods=['POST'])
@cross_origin()
def analyze_topic():
    topic = request.json['topic']
    result = model.analyze_tweet(topic)

    return json.dumps(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)