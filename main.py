"""
WSGI adapter file for running the Django application with Gunicorn
"""
import os
import sys

# Add the project directory to the sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fakenewsdetector.settings')

# Download required NLTK data before importing Django
try:
    import nltk
    print("Downloading NLTK data...")
    nltk.download('punkt', quiet=False)
    nltk.download('stopwords', quiet=False)
    nltk.download('wordnet', quiet=False)
    print("NLTK data download completed.")
except Exception as e:
    print(f"Error downloading NLTK data: {e}")

# Create the ML model directory if it doesn't exist
model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'detector', 'ml_model')
os.makedirs(model_dir, exist_ok=True)
print(f"Created ML model directory at: {model_dir}")

# Import the WSGI application
from fakenewsdetector.wsgi import application as app