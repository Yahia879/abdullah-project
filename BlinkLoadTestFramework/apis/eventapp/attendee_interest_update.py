import json

from apis import base_api


def create_message():
    message_json_body = {}
    message_json_body["email"] ,message_json_body["id"] = base_api.generate_email_user_id()
    message_json_body["message_id"] = base_api.generate_id()
    message_json_body["interest_topic_category_ids"] = base_api.generate_list()
    message_json_body["event_goal_ids"] = base_api.generate_list()
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