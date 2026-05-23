import json
from apis import base_api

def get_endpoint():
    # Add all required query parameters
    event_id = base_api.generate_event_id()
    template_type = "sessions"  
    offset = 0  
    limit = 10  
    
    return f"/api/v3/mobile-logistics/notification-update-templates?event_id=4531&template_type=sessions"

def get_method():
    return "GET"

def get_headers():
    return base_api.headers 