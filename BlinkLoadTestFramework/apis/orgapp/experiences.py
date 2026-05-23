import json
from apis import base_api

def get_experiences_stats_endpoint():
    event_id = base_api.generate_event_id()
    return f"/api/v3/mobile-logistics/itineraries/experiences/stats?event_id={event_id}"

def get_experiences_stats_method():
    return "GET"

def create_calendar_activity_message():
    message_json_body = {}
    message_json_body["event_id"] = base_api.generate_event_id()
    message_json_body["date"] = "2025-05-13"  # from 2-8 june
    return json.dumps(message_json_body.copy())

def get_calendar_activity_endpoint():
    return "/api/v3/mobile-logistics/calender-activity-indicator"

def get_calendar_activity_method():
    return "POST"

def get_headers():
    return base_api.headers 