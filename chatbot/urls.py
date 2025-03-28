#import sys
#print("Importing chatbot/urls.py...")
#print("Modules currently loaded:", list(sys.modules.keys()))

from django.urls import path
from .views import chatbot_view, quiz_view, admin_visualization_view, home_view

urlpatterns = [
    path('', home_view, name='home'),  # Map root URL (/) to home_view
    path('chatbot/', chatbot_view, name='chatbot'),
    path('quiz/', quiz_view, name='quiz'),
    path('admin_visualization/', admin_visualization_view, name='admin_visualization'),
]

print("chatbot/urls.py loaded successfully!")
