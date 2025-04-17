from django.db import models

# Create your models here.
class DetectionResult(models.Model):
    """
    Model to store detection results for analysis and improvement
    """
    input_text = models.TextField()
    input_url = models.URLField(blank=True, null=True)
    is_fake = models.BooleanField()
    confidence_score = models.FloatField()
    ml_prediction = models.BooleanField()
    openai_prediction = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{'Fake' if self.is_fake else 'Real'} news with {self.confidence_score*100:.1f}% confidence"
