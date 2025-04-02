# Importing Django's AppConfig class which is used to configure application-specific settings
from django.apps import AppConfig

# Define configuration for the 'core' app of the Django project
class CoreConfig(AppConfig):
    # Name of the app, used by Django to reference this app
    name = 'core'
