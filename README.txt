FAKE NEWS DETECTOR
================

A web-based tool that uses AI and machine learning to detect fake news.

HOW IT WORKS
-----------

This application helps you determine if a news article is likely to be fake or legitimate using:

1. Machine Learning: Trained on datasets of real and fake news to identify patterns
2. OpenAI API: Enhanced analysis using advanced language models (for URL analysis)
3. Web Scraping: Automatically extracts and analyzes content from news websites

FEATURES
--------

- Analyze news by pasting text directly
- Analyze news by providing a URL
- Get confidence scores for each prediction
- See key factors that influenced the decision
- View trending news with the option to analyze any story

HOW TO USE
----------

TEXT ANALYSIS:
1. Select "Text Analysis" tab
2. Paste the news article text
3. Click "Analyze"
4. View the analysis results

URL ANALYSIS:
1. Select "URL Analysis" tab
2. Enter the URL of a news article
3. Click "Analyze"
4. View the combined ML and OpenAI analysis

SAMPLE ARTICLES:
- Use the provided examples of known fake and real news to test the system

REQUIREMENTS
-----------

- Python 3.8+
- Django
- NLTK (with punkt, stopwords, and wordnet datasets)
- scikit-learn
- pandas
- trafilatura (for web scraping)
- OpenAI API key (for enhanced analysis)
- News API key (for trending news)

SETUP
-----

1. Install dependencies:
   pip install -r requirements-guide.txt

2. Set environment variables:
   - OPENAI_API_KEY: Your OpenAI API key
   - NEWS_API_KEY: Your News API key

3. Run the application:
   python manage.py runserver

   OR with Gunicorn (production):
   gunicorn --bind 0.0.0.0:5000 main:app

TRAINING DATA
------------

The machine learning model is trained on:
- True.csv: Collection of verified real news
- Fake.csv: Collection of verified fake news
- scraped.csv: Additional web-scraped data

TECHNICAL DETAILS
---------------

- Frontend: HTML, CSS (Bootstrap), JavaScript
- Backend: Django (Python)
- ML: scikit-learn RandomForestClassifier
- Text processing: NLTK
- Advanced analysis: OpenAI GPT
- Web scraping: Trafilatura
- Visualization: Chart.js

Contact: your@email.com for support or questions.