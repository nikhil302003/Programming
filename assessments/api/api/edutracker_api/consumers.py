import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Student


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        if isinstance(self.user, AnonymousUser):
            await self.close()
            return
        
        # Get student profile for the user
        self.student = await self.get_student_profile()
        
        if not self.student:
            await self.close()
            return
        
        # Create a unique group name for this student
        self.group_name = f"student_{self.student.id}"
        
        # Join the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave the group
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
    
    async def notification_message(self, event):
        """Handle notification messages sent to the group."""
        notification = event['notification']
        
        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': notification
        }))
    
    @database_sync_to_async
    def get_student_profile(self):
        """Get student profile for the authenticated user."""
        try:
            return Student.objects.get(user=self.user)
        except Student.DoesNotExist:
            return None


class CourseUpdatesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        if isinstance(self.user, AnonymousUser):
            await self.close()
            return
        
        # Get student profile for the user
        self.student = await self.get_student_profile()
        
        if not self.student:
            await self.close()
            return
        
        # Join a general updates group
        self.group_name = "course_updates"
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave the group
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
    
    async def course_update(self, event):
        """Handle course update messages."""
        update_data = event['update']
        
        await self.send(text_data=json.dumps({
            'type': 'course_update',
            'update': update_data
        }))
    
    @database_sync_to_async
    def get_student_profile(self):
        """Get student profile for the authenticated user."""
        try:
            return Student.objects.get(user=self.user)
        except Student.DoesNotExist:
            return None
