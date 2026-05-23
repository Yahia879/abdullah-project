import json
import random
from apis import base_api

def get_show_item_endpoint():
    event_id = base_api.generate_event_id()
    admission_item_type = "user_badges"
    badge_qr_code = base_api.generate_badge_qr_code()
    return f"/api/v3/admission-portal/admission-items/show-item?event_id={event_id}&admission_item_type={admission_item_type}&badge_qr_code={badge_qr_code}"

def get_show_item_method():
    return "GET"

def create_send_verification_message():
    message_json_body = {}
    message_json_body["admission_item_type"] = "user_badges"
    message_json_body["sso_id"] = base_api.generate_user_id()
    message_json_body["printing_type"] = "qr_code" #or manual_search
    return json.dumps(message_json_body.copy())

def get_send_verification_endpoint():
    event_id = base_api.generate_event_id()
    admission_item_type = "user_badges"  # Example value, could be "ticket", "badge", etc.
    sso_id = base_api.generate_user_id()
    return f"/api/v3/admission-portal/admission-items/send-print-verification-code?event_id={event_id}&admission_item_type={admission_item_type}&sso_id={sso_id}"

def get_send_verification_method():
    return "POST"

def create_verify_code_message():
    message_json_body = {}
    message_json_body["admission_item_type"] = "user_badges"
    message_json_body["sso_id"] = base_api.generate_user_id()
    message_json_body["printing_type"] = "qr_code" #or manual_search
    message_json_body["verification_code"] = "123456"  # Example code, adjust as needed
    return json.dumps(message_json_body.copy())

def get_verify_code_endpoint():
    return "/api/v3/admission-portal/admission-items/verify-print-verification-code"

def get_verify_code_method():
    return "POST"

def create_print_message():
    message_json_body = {}
    message_json_body["admission_item_type"] = "user_badges"
    message_json_body["sso_id"] = base_api.generate_user_id()
    message_json_body["printing_type"] = "qr_code" #or manual_search
    return json.dumps(message_json_body.copy())

def get_print_endpoint():
    # Add the same query parameters as other endpoints
    item_id = base_api.generate_id()
    event_id = base_api.generate_event_id()
    admission_item_type = "badge"  # Example value, could be "ticket", "badge", etc.
    sso_id = base_api.generate_user_id()
    
    # Add the printing_type parameter with randomly selected value
    printing_type = random.choice(["qr_code", "manual_search"])
    
    # Construct the URL with all query params
    return f"/api/v3/admission-portal/admission-items/print?id={item_id}&event_id={event_id}&admission_item_type={admission_item_type}&sso_id={sso_id}&printing_type={printing_type}"

def get_print_method():
    return "PATCH"

def get_headers():
    return base_api.admission_headers