from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import re

app = Flask(__name__)


def clean_text(text):
    """Clean the text by removing special characters, links, etc."""
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'@\w+', '', text)  # Remove mentions
    text = re.sub(r'#\w+', '', text)  # Remove hashtags
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text


def analyze_sentiment(text):
    """Analyze sentiment of the given text using TextBlob."""
    # Clean the text
    cleaned_text = clean_text(text)

    # Create TextBlob object
    analysis = TextBlob(cleaned_text)

    # Determine sentiment category
    polarity = analysis.sentiment.polarity

    if polarity > 0.1:
        sentiment = "Positive"
        color = "#28a745"  # Green
    elif polarity < -0.1:
        sentiment = "Negative"
        color = "#dc3545"  # Red
    else:
        sentiment = "Neutral"
        color = "#6c757d"  # Gray

    # Prepare results
    result = {
        "text": text,
        "polarity": round(polarity, 2),
        "subjectivity": round(analysis.sentiment.subjectivity, 2),
        "sentiment": sentiment,
        "color": color
    }

    return result


@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """API endpoint to analyze sentiment of the given text."""
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = analyze_sentiment(text)
    return jsonify(result)


@app.route('/analyze-form', methods=['POST'])
def analyze_form():
    """Handle form submission for sentiment analysis."""
    text = request.form.get('text', '')

    if not text:
        return render_template('index.html', error="Please enter some text to analyze")

    result = analyze_sentiment(text)
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)