from django.db import models
from apps.core.models import User

class Conversation(models.Model):
    """Represents a conversation between two users"""
    participant_a = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_a')
    participant_b = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_b')
    last_message = models.TextField(blank=True, help_text='Preview of the last message')
    last_at = models.DateTimeField(auto_now=True, help_text='Timestamp of last message')
    unread_a = models.IntegerField(default=0, help_text='Unread count for participant A')
    unread_b = models.IntegerField(default=0, help_text='Unread count for participant B')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-last_at']
        unique_together = ('participant_a', 'participant_b')
        indexes = [
            models.Index(fields=['participant_a', 'participant_b']),
        ]
    
    def __str__(self):
        return f"Conversation {self.id}: {self.participant_a.username} ↔ {self.participant_b.username}"


class Message(models.Model):
    """Individual message in a conversation"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    body = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender.username} in Conversation {self.conversation.id}"


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('order', 'Order'),
        ('message', 'Message'),
        ('alert', 'Alert'),
        ('system', 'System'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} for {self.user.username}"


# Legacy models (kept for backward compatibility, can be deprecated)
class ConversationMessage(models.Model):
    """Legacy model - use Message and Conversation instead"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='legacy_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sender.username} in {self.conversation.id}"
