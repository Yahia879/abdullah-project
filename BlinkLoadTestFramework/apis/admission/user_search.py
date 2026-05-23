import json
from apis import base_api

def get_endpoint():
    # Add all required query parameters
    event_id = base_api.generate_event_id()
    search_value = base_api.generate_name()
    limit = 10  # Default limit for pagination
    offset = 0  # Default offset starting from beginning
    return f"/api/v3/admission-portal/users/search?event_id={event_id}&search={search_value}&limit={limit}&offset={offset}"

def get_method():
    return "GET"

def get_headers():
    return base_api.admission_headers