import os

api_key = os.getenv('CHOICES_API_KEY', '')
google_maps_api_key = os.getenv('GOOGLE_API_KEY', '')

try:
    import config
    api_key = config.api_key
    google_maps_api_key = config.google_maps_api_key
except:
    pass