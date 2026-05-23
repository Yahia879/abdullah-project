import json
from apis import base_api

def create_message():
    message_json_body = {}
    message_json_body["event_id"] = base_api.generate_event_id()
    message_json_body["search"] = ""
    message_json_body["limit"] = 10
    message_json_body["offset"] = 0
    message_json_body["bookmarked"] = True
    message_json_body["filter_types"] = ["attendee"]
    return json.dumps(message_json_body.copy())

def get_endpoint():
    # Add event_id as a query parameter
    event_id = base_api.generate_event_id()
    return f"/api/v3/mobile-logistics/home/attendees?event_id={event_id}"

def get_method():
    return "PATCH"

def get_headers():
    return base_api.headers 