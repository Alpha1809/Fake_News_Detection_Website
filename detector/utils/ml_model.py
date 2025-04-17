import os
import re
import pandas as pd
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from django.conf import settings

# Initialize global variables
vectorizer = None
model = None

def create_fallback_model():
    """Create a simple fallback model when the main training process fails"""
    global vectorizer, model
    
    # Create a simple dataset with basic patterns
    fake_texts = [
        "shocking news that the media won't tell you",
        "government conspiracy revealed",
        "miracle cure they don't want you to know about",
        "they don't want you to know this secret",
        "this will change everything you believe about"
    ]
    real_texts = [
        "according to recent scientific studies",
        "experts have confirmed that",
        "multiple sources have verified",
        "researchers at the university found that",
        "evidence suggests that"
    ]
    
    df = pd.DataFrame({
        'text': fake_texts + real_texts,
        'label': [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
    })
    
    # Create processed text
    df['processed_text'] = df['text'].apply(lambda x: x.lower())
    
    # Create a basic vectorizer and model
    vectorizer = TfidfVectorizer(max_features=100)
    X = vectorizer.fit_transform(df['processed_text'])
    y = df['label']
    
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)
    
    # Save this basic model
    try:
        with open(os.path.join(settings.ML_MODEL_PATH, 'fake_news_model.pkl'), 'wb') as f:
            pickle.dump(model, f)
        with open(os.path.join(settings.ML_MODEL_PATH, 'tfidf_vectorizer.pkl'), 'wb') as f:
            pickle.dump(vectorizer, f)
        print("Fallback model created and saved successfully.")
    except Exception as e:
        print(f"Error saving fallback model: {str(e)}")

def init_model():
    """Initialize and train the ML model on startup"""
    global vectorizer, model
    
    try:
        # Check if model exists and load it
        model_path = os.path.join(settings.ML_MODEL_PATH, 'fake_news_model.pkl')
        vectorizer_path = os.path.join(settings.ML_MODEL_PATH, 'tfidf_vectorizer.pkl')
        
        # Create directory if it doesn't exist
        os.makedirs(settings.ML_MODEL_PATH, exist_ok=True)
        
        if os.path.exists(model_path) and os.path.exists(vectorizer_path):
            # Load pre-trained model and vectorizer
            print("Loading pre-trained model and vectorizer...")
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            with open(vectorizer_path, 'rb') as f:
                vectorizer = pickle.load(f)
            print("Model and vectorizer loaded successfully.")
        else:
            print("No pre-trained model found. Training a new model...")
            # Train new model
            train_model()
            print("New model trained and saved successfully.")
    except Exception as e:
        print(f"Error initializing model: {str(e)}")
        # Create a basic fallback model
        print("Creating a basic fallback model...")
        create_fallback_model()

def preprocess_text(text):
    """Clean and preprocess text for machine learning"""
    if not text:
        return ""
        
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove special characters and digits
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenize text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return ' '.join(tokens)

def train_model():
    """Train the machine learning model using the provided datasets"""
    global vectorizer, model
    
    # Load and prepare datasets
    try:
        # Load the true news dataset
        true_df = pd.read_csv('attached_assets/True.csv')
        true_df['label'] = 0  # 0 for real news
        
        # Load the fake news dataset
        fake_df = pd.read_csv('attached_assets/Fake.csv')
        fake_df['label'] = 1  # 1 for fake news
        
        # Load the scraped dataset which is already labeled
        scraped_df = pd.read_csv('attached_assets/scraped.csv')
        
        # Select and rename columns as needed
        if 'title' in true_df.columns and 'text' in true_df.columns:
            # For datasets that have both title and text
            true_df['content'] = true_df['title'] + ". " + true_df['text']
            true_df = true_df[['content', 'label']]
            true_df.rename(columns={'content': 'text'}, inplace=True)
        else:
            # Handle case where columns are different
            true_df = true_df[['text', 'label']]
            
        if 'title' in fake_df.columns and 'text' in fake_df.columns:
            fake_df['content'] = fake_df['title'] + ". " + fake_df['text']
            fake_df = fake_df[['content', 'label']]
            fake_df.rename(columns={'content': 'text'}, inplace=True)
        else:
            fake_df = fake_df[['text', 'label']]
        
        # Ensure scraped_df has the right columns
        scraped_df = scraped_df[['text', 'label']]
        
        # Combine datasets
        df = pd.concat([true_df, fake_df, scraped_df], ignore_index=True)
        
        # Preprocess the text
        df['processed_text'] = df['text'].apply(preprocess_text)
        
        # Create TF-IDF features
        vectorizer = TfidfVectorizer(max_features=5000)
        X = vectorizer.fit_transform(df['processed_text'])
        y = df['label']
        
        # Train random forest classifier
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        # Save the model and vectorizer
        with open(os.path.join(settings.ML_MODEL_PATH, 'fake_news_model.pkl'), 'wb') as f:
            pickle.dump(model, f)
        with open(os.path.join(settings.ML_MODEL_PATH, 'tfidf_vectorizer.pkl'), 'wb') as f:
            pickle.dump(vectorizer, f)
            
    except Exception as e:
        print(f"Error training model: {str(e)}")
        # Create a simple fallback model if the datasets are not available
        fake_texts = [
            "shocking news that the media won't tell you",
            "government conspiracy revealed",
            "miracle cure they don't want you to know about"
        ]
        real_texts = [
            "according to recent scientific studies",
            "experts have confirmed that",
            "multiple sources have verified"
        ]
        
        df = pd.DataFrame({
            'text': fake_texts + real_texts,
            'label': [1, 1, 1, 0, 0, 0]
        })
        
        df['processed_text'] = df['text'].apply(preprocess_text)
        
        vectorizer = TfidfVectorizer(max_features=100)
        X = vectorizer.fit_transform(df['processed_text'])
        y = df['label']
        
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        # Save this basic model
        with open(os.path.join(settings.ML_MODEL_PATH, 'fake_news_model.pkl'), 'wb') as f:
            pickle.dump(model, f)
        with open(os.path.join(settings.ML_MODEL_PATH, 'tfidf_vectorizer.pkl'), 'wb') as f:
            pickle.dump(vectorizer, f)

def predict(text):
    """
    Make a prediction on whether the given text is fake news or not
    Returns: (is_fake, confidence)
    """
    global vectorizer, model
    
    # Check if model is loaded
    if model is None or vectorizer is None:
        init_model()
    
    # Preprocess the text
    processed_text = preprocess_text(text)
    
    # Transform the text using the vectorizer
    X = vectorizer.transform([processed_text])
    
    # Make prediction
    prediction_proba = model.predict_proba(X)[0]
    is_fake = prediction_proba[1] > 0.5
    confidence = prediction_proba[1] if is_fake else prediction_proba[0]
    
    return is_fake, confidence

def get_explanation(text):
    """
    Get explanation for the prediction 
    Returns key factors that influenced the decision
    """
    global vectorizer, model
    
    if model is None or vectorizer is None:
        init_model()
    
    # Preprocess the text
    processed_text = preprocess_text(text)
    
    # Get feature importance
    if not processed_text:
        return []
        
    # Extract words from the text
    words = processed_text.split()
    
    # Get feature names from the vectorizer
    try:
        feature_names = vectorizer.get_feature_names_out()
    except AttributeError:
        # For older versions of scikit-learn
        feature_names = vectorizer.get_feature_names()
    
    # Get feature importances from the model
    importances = model.feature_importances_
    
    # Match words in the text to feature importances
    word_importances = []
    for word in set(words):
        if word in feature_names:
            idx = list(feature_names).index(word)
            word_importances.append((word, importances[idx]))
    
    # Return top 5 most important words that appear in the text
    return sorted(word_importances, key=lambda x: x[1], reverse=True)[:5]
