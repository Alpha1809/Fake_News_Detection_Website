import requests
import trafilatura
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_website_text(url):
    """
    Extract main text content from a website URL
    Uses trafilatura for efficient text extraction
    """
    try:
        # Check if URL is valid
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return None
        
        # Get the content using trafilatura
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded)
        
        # If trafilatura fails, try a backup method with BeautifulSoup
        if not text:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(['script', 'style', 'meta', 'noscript']):
                script.extract()
            
            # Get text from p, h1-h6, and article tags
            paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'article'])
            text = ' '.join([p.get_text() for p in paragraphs])
        
        return text.strip()
        
    except Exception as e:
        print(f"Error scraping URL {url}: {str(e)}")
        return None
