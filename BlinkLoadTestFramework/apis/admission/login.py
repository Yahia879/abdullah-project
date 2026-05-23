import json
from apis import base_api

def create_message():
    message_json_body = {}
    message_json_body["email"] = base_api.generate_email()
    message_json_body["password"] = "password123" 
    return json.dumps(message_json_body.copy())

def get_endpoint():
    return "/api/v3/admission-portal/login"

def get_method():
    return "POST"

def get_headers():
    return base_api.admission_headers