import json
import random
import uuid
from apis import base_api

def get_sessions_endpoint():
    event_id = base_api.generate_event_id()
    is_ticketed = random.choice(["true", "false"])
    return f"/api/v3/mobile-logistics/scanner/sessions?event_id={event_id}&is_ticketed={is_ticketed}"

def get_sessions_method():
    return "GET"

def get_check_user_access_endpoint():
    return f"/api/v3/mobile-logistics/itineraries/sessions/931/check-user-access?qr_code=44b90d0c-2f58-4ce7-bc43-f439eedff4a4&event_id=112"

def get_check_user_access_method():
    return "GET"

def get_checkin_endpoint():
    event_id = base_api.generate_event_id()
    session_id = base_api.generate_session_id()
    qr_code = base_api.generate_user_id()
    return f"/api/v3/mobile-logistics/itineraries/check-in-without-validation?event_id=112"

def create_checkin_message():
    message_json_body = {}
    message_json_body["event_id"] = "112"
    message_json_body["session_id"] = "931"
    message_json_body["qr_code"] = "8099bdf2-23ae-424f-94f7-932f5b751ca0"
    return json.dumps(message_json_body.copy())

def get_checkin_method():
    return "PATCH"

def get_session_scan_logs_endpoint():
    guest_id = base_api.generate_user_id()
    event_id = base_api.generate_event_id()
    limit = 10
    offset = 0
    return f"/api/v3/mobile-logistics/session-scan-logs?guest_id=ba6216cc-76e2-417a-bf9d-d9f8ef0acc42&event_id=112&limit=10&offset=0"

def get_session_scan_logs_method():
    return "GET"

def get_headers():
    return base_api.headers 