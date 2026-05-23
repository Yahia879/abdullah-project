import json
from apis import base_api

def create_message():
    message_json_body = {}
    message_json_body["email"] = base_api.generate_email()
    message_json_body["password"] = "password123"  # Using a static password for testing
    return json.dumps(message_json_body.copy())

def get_endpoint():
    return "/api/login"

def get_method():
    return "POST"

def get_headers():
    return base_api.headers 