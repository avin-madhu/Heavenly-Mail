from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class ScheduledEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=100)
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    send_on = models.DateTimeField(null=True, blank=True)  
    last_active = models.DateTimeField(default=timezone.now)
    time_limit = models.DurationField(default=timedelta(days=365)) 
    sent = models.BooleanField(default=False) 
    
    def __str__(self):
        return f'Email to {self.recipient_name}'
    
    def is_ready_to_send(self):
        """Check if the email should be sent based on inactivity or specific send date."""
        if self.confirmed_by_contact or (self.send_on and timezone.now() >= self.send_on):
            return True
        elif timezone.now() - self.last_active >= self.time_limit:
            return True
        return False