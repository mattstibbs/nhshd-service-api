import os

api_key = os.getenv('CHOICES_API_KEY', '')
google_maps_api_key = os.getenv('GOOGLE_API_KEY', '')
account_sid = os.getenv('ACCOUNT_SID', '')
auth_token = os.getenv('AUTH_TOKEN', '')
twilio_number = os.getenv('TWILIO_NUMBER', '')

try:
    import config
    api_key = config.api_key
    google_maps_api_key = config.google_maps_api_key
    account_sid = config.account_sid
    auth_token = config.auth_token
    twilio_number = config.twilio_number
except:
    pass