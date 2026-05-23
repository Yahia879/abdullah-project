import json
from apis import base_api

def get_venues_endpoint():
    # Add event_id as a query parameter
    event_id = base_api.generate_event_id()
    return f"/api/v3/mobile-logistics/home/venues?event_id={event_id}"

def get_venues_method():
    return "GET"

def get_venue_sessions_endpoint():
    # Generate a dynamic venue ID instead of using a static one
    venue_id = "7192"
    
    # Add event_id as a query parameter
    event_id = base_api.generate_event_id()
    
    # Construct URL with both path parameter and query parameters
    return f"/api/v3/mobile-logistics/home/venues/{venue_id}/sessions?event_id={event_id}&venue_id={venue_id}"

def get_venue_sessions_method():
    return "GET"

def get_headers():
    return base_api.headers 