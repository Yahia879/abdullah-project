import json

from apis import base_api


def create_message():
    message_json_body = {}
    message_json_body["first_name"] = base_api.generate_name()
    message_json_body["last_name"] = base_api.generate_name()
    message_json_body["email"] ,message_json_body["id"] = base_api.generate_email_user_id()
    message_json_body["photo"] = base_api.generate_string()
    message_json_body["city"] = base_api.generate_string()
    message_json_body["country"] = base_api.generate_country()
    message_json_body["job_title"] = base_api.generate_string()
    message_json_body["company_name"] = base_api.generate_string()
    message_json_body["is_discoverable"] = base_api.generate_bool()
    message_json_body["linkedin_url"] = base_api.generate_url()
    message_json_body["bio"] = base_api.generate_string()
    message_json_body["industry"] = base_api.generate_industry()
    message_json_body["company_size"] = base_api.generate_company_size()
    message_json_body["budget_range"] = base_api.generate_budget_range()
    message_json_body["age_group"] = base_api.generate_age_group()
    message_json_body["event_id"] = base_api.generate_event_id()
    message_json_body["message_id"] = base_api.generate_id()
    return json.dumps(message_json_body.copy())


def create_message_json():
    message_json = str(create_message())
    message_json = message_json.replace("'", '\"')
    message_json_body = {
        "message_module_name": "User",
        "message_root_path": "blink_ga_firestore",
        "message_key": "AttendeeUpdated",
        "message_version": "V1",
        "message_data": message_json
    }
    return message_json_body.copy()