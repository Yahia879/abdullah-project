import json

from apis import base_api


def create_message():
    message_json_body = {}
    message_json_body["attendee_id"] = base_api.generate_user_id()
    message_json_body["fcm_token"] = base_api.generate_string()
    message_json_body["message_id"] = base_api.generate_id()
    return json.dumps(message_json_body.copy())


def create_message_json():
    message_json = str(create_message())
    message_json = message_json.replace("'", '\"')
    message_json_body = {
        "message_version": "V1",
        "message_module_name": "Attendee",
        "message_root_path": "blink_ga_firestore",
        "message_key": "AttendeeGaFcmTokenUpdated",
        "message_data": message_json
    }
    return message_json_body.copy()