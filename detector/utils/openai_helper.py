import os
import json
from django.conf import settings
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def analyze_text(text):
    """
    Use OpenAI to analyze if text is fake news
    Returns: (is_fake, confidence)
    """
    if not settings.OPENAI_API_KEY:
        raise ValueError("OpenAI API key is not configured")
        
    # Truncate text if too long (OpenAI has token limits)
    max_chars = 4000
    if len(text) > max_chars:
        text = text[:max_chars] + "..."
    
    try:
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert at detecting fake news and misinformation. "
                        "Analyze the following news text and determine if it's likely to be fake news or real news. "
                        "Consider factors like: sensationalist language, emotional manipulation, lack of cited sources, "
                        "political bias, inconsistencies, implausible claims, etc. "
                        "Respond with JSON in this format: {'is_fake': boolean, 'confidence': float between 0 and 1, 'explanation': string}"
                    )
                },
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        result = json.loads(response.choices[0].message.content)
        return result["is_fake"], result["confidence"]
        
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        # Return None values so we can fall back to ML model
        return None, 0
