from rest_framework import serializers
from .models import Message, Conversation, ConversationMessage, Notification

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    recipient_name = serializers.CharField(source='recipient.username', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_name', 'recipient', 'recipient_name', 'subject', 'content', 'is_read', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']

class ConversationMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    
    class Meta:
        model = ConversationMessage
        fields = ['id', 'sender', 'sender_name', 'content', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    messages = ConversationMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'last_message', 'messages', 'updated_at']
        read_only_fields = ['id', 'updated_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'notification_type', 'title', 'message', 'is_read', 'link', 'created_at']
        read_only_fields = ['id', 'created_at']
