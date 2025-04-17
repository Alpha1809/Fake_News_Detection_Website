# Fake News Detector

A Django-based web application that detects fake news from text or URLs using Machine Learning and OpenAI API, while displaying trending news stories.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technical Architecture](#technical-architecture)
- [Installation](#installation)
- [How to Use](#how-to-use)
- [API Keys](#api-keys)
- [Data](#data)
- [Project Structure](#project-structure)
- [Machine Learning Model](#machine-learning-model)
- [OpenAI Integration](#openai-integration)
- [Web Scraping](#web-scraping)

## Overview

The Fake News Detector is an AI-powered web application designed to analyze news articles and determine the likelihood that they contain false or misleading information. The system uses a combination of machine learning models and OpenAI's GPT to evaluate the authenticity of news content.

## Features

- **Text Analysis**: Directly analyze news article text through a user-friendly interface
- **URL Analysis**: Analyze a news article by providing its URL (web scraping + ML/AI analysis)
- **Dual Detection System**: Combines traditional machine learning with OpenAI for enhanced accuracy
- **Confidence Scores**: Provides confidence percentage for each prediction
- **Key Factors Identification**: Highlights key phrases and patterns that influenced the decision
- **Trending News Display**: Shows latest trending news with the ability to analyze any of them
- **Responsive Design**: Works seamlessly across desktop and mobile devices

## Technical Architecture

The application is built on the following core technologies:

- **Backend**: Django (Python)
- **Machine Learning**: scikit-learn (RandomForestClassifier)
- **Text Processing**: NLTK for text preprocessing and feature extraction
- **AI Integration**: OpenAI API for enhanced text analysis
- **Web Scraping**: Trafilatura for efficient content extraction
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Data Visualization**: Chart.js for displaying confidence scores

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fake-news-detector.git
   cd fake-news-detector
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements-guide.txt
   ```

3. Download NLTK data:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('wordnet')
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following:
   ```
   SECRET_KEY=your_django_secret_key
   OPENAI_API_KEY=your_openai_api_key
   NEWS_API_KEY=your_news_api_key
   ```

5. Run database migrations:
   ```
   python manage.py migrate
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```
   
7. For production, use Gunicorn:
   ```
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

## How to Use

### Analyzing Text Content

1. Go to the application homepage
2. Select the "Text Analysis" tab
3. Paste the full text of a news article in the text area
4. Click "Analyze" to process the text
5. View the results, including:
   - Whether the content is likely fake or real
   - Confidence percentage
   - Key factors that influenced the decision

### Analyzing a News Article URL

1. Go to the application homepage
2. Select the "URL Analysis" tab
3. Paste the URL of a news article
4. Click "Analyze" to process the URL
5. The system will:
   - Scrape the content from the URL
   - Analyze it using both machine learning and OpenAI (if configured)
   - Display comprehensive results

### Exploring Trending News

1. Scroll down to the "Trending News" section
2. View the latest trending news stories
3. Click "Analyze" on any story to immediately analyze it for authenticity
4. Click "Read More" to visit the original source

## API Keys

The application requires the following API keys:

- **OpenAI API Key**: For enhanced text analysis (optional but recommended)
- **News API Key**: For fetching trending news stories

These keys should be stored as environment variables or in a `.env` file.

## Data

The machine learning model is trained on labeled datasets of fake and real news articles. The project includes:

- `True.csv`: A dataset containing verified real news articles
- `Fake.csv`: A dataset containing verified fake news articles
- `scraped.csv`: Additional data collected through web scraping

The model is trained to identify patterns, language structures, and content characteristics that differentiate fake news from reliable content.

## Project Structure

```
fake-news-detector/
│
├── detector/                # Main Django app folder
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   ├── static/              # CSS, JS, and image files
│   ├── utils/               # Utility modules
│   │   ├── ml_model.py      # Machine learning model
│   │   ├── openai_helper.py # OpenAI integration
│   │   ├── web_scraper.py   # Web scraping functionality
│   │   └── news_api.py      # News API integration
│   ├── admin.py             # Admin interface configuration
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   └── urls.py              # URL routing
│
├── fakenewsdetector/        # Project settings folder
│   ├── settings.py          # Project settings
│   ├── urls.py              # Project URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
│
├── attached_assets/         # Training datasets
│   ├── True.csv
│   ├── Fake.csv
│   └── scraped.csv
│
├── main.py                  # WSGI entry point
├── manage.py                # Django management script
├── requirements-guide.txt   # List of dependencies
└── README.md                # Project documentation
```

## Machine Learning Model

The core detection engine uses a RandomForestClassifier from scikit-learn. The model's workflow includes:

1. **Data Preprocessing**:
   - Text cleaning (removing special characters, HTML tags)
   - Tokenization (breaking text into individual words)
   - Stop word removal (filtering out common words like "the", "and")
   - Lemmatization (reducing words to their base form)

2. **Feature Extraction**:
   - TF-IDF Vectorization (Term Frequency-Inverse Document Frequency)
   - This converts text into numerical features for the machine learning model

3. **Classification**:
   - The RandomForest algorithm analyzes the features
   - Outputs a prediction (fake or real) and a confidence score

4. **Explanation Generation**:
   - Identifies the most important words/phrases that influenced the decision
   - Calculates importance scores for each factor

## OpenAI Integration

For enhanced accuracy, the system can integrate with OpenAI's GPT model:

1. When a URL is analyzed, both the ML model and OpenAI evaluate the content
2. The system combines predictions, using the one with higher confidence
3. This hybrid approach leverages both traditional ML and advanced language models

## Web Scraping

The URL analysis feature uses Trafilatura to efficiently extract the main content from news websites:

1. The application sends a request to the provided URL
2. Trafilatura identifies and extracts the main article text
3. The extracted text is then processed by the detection system
4. This allows analysis of articles without manual copy-pasting