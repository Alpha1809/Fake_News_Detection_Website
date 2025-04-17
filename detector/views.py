import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import DetectionResult
from .utils import ml_model, web_scraper, openai_helper, news_api

def index(request):
    """Home page view with form for text/URL input"""
    trending = news_api.get_trending_news()
    return render(request, 'detector/index.html', {'trending': trending})

@csrf_exempt
def detect(request):
    """Handle detection form submission"""
    if request.method == 'POST':
        # Get input data
        news_text = request.POST.get('news_text', '')
        news_url = request.POST.get('news_url', '')
        
        # Track if we're using ML only or ML+OpenAI
        using_openai = False
        scraped_text = ''
        
        # Process based on input type
        if news_url:
            try:
                # Scrape the content from the URL
                scraped_text = web_scraper.get_website_text(news_url)
                
                if not scraped_text:
                    return JsonResponse({
                        'error': 'Could not extract text from the provided URL. Please try a different URL or paste the text directly.'
                    }, status=400)
                
                # Use the scraped text for ML prediction
                ml_prediction, ml_confidence = ml_model.predict(scraped_text)
                
                # If OpenAI API key is available, use it for additional analysis
                if settings.OPENAI_API_KEY:
                    using_openai = True
                    openai_prediction, openai_confidence = openai_helper.analyze_text(scraped_text)
                    
                    # Combine predictions (weighted average)
                    is_fake = ml_prediction if ml_confidence > openai_confidence else openai_prediction
                    confidence_score = max(ml_confidence, openai_confidence)
                else:
                    is_fake = ml_prediction
                    confidence_score = ml_confidence
                    openai_prediction = None
                    
            except Exception as e:
                return JsonResponse({
                    'error': f'Error processing URL: {str(e)}'
                }, status=400)
        
        elif news_text:
            # Use ML model for text prediction
            ml_prediction, ml_confidence = ml_model.predict(news_text)
            is_fake = ml_prediction
            confidence_score = ml_confidence
            openai_prediction = None
            
        else:
            return JsonResponse({
                'error': 'Please provide either text or a URL to analyze'
            }, status=400)
            
        # Save the result
        result = DetectionResult.objects.create(
            input_text=news_text if news_text else scraped_text,
            input_url=news_url,
            is_fake=is_fake,
            confidence_score=confidence_score,
            ml_prediction=ml_prediction,
            openai_prediction=openai_prediction
        )
        
        # Return result ID for redirect
        return JsonResponse({
            'result_id': result.id
        })
        
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def results(request, result_id):
    """Display detection results"""
    result = get_object_or_404(DetectionResult, id=result_id)
    trending = news_api.get_trending_news()
    
    # Get explanation factors
    explanation = ml_model.get_explanation(result.input_text)
    
    return render(request, 'detector/results.html', {
        'result': result,
        'explanation': explanation,
        'trending': trending
    })

def trending_news(request):
    """API endpoint to get trending news"""
    trending = news_api.get_trending_news()
    return JsonResponse({'trending': trending})
