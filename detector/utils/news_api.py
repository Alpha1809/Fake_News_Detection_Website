import requests
import json
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache

def get_trending_news():
    """
    Get the top 10 trending news articles from News API
    Uses caching to avoid repeated API calls
    """
    # Check if we have cached results
    cached_news = cache.get('trending_news')
    if cached_news:
        return cached_news
    
    # If no News API key, return empty list
    if not settings.NEWS_API_KEY:
        return []
    
    api_key = settings.NEWS_API_KEY
    
    # Calculate date for the last 24 hours
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    from_date = yesterday.strftime('%Y-%m-%d')
    
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('status') == 'ok':
            articles = data.get('articles', [])
            
            # Process articles
            trending_news = []
            for i, article in enumerate(articles[:10]):  # Limit to top 10
                trending_news.append({
                    'id': i + 1,
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', ''),
                    'published_at': article.get('publishedAt', '')
                })
            
            # Cache results for 30 minutes
            cache.set('trending_news', trending_news, 30 * 60)
            
            return trending_news
        else:
            print(f"News API error: {data.get('message', 'Unknown error')}")
            return []
            
    except Exception as e:
        print(f"Error fetching trending news: {str(e)}")
        return []
