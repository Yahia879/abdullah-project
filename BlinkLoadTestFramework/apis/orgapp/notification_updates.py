import json
import random
from apis import base_api

def create_message():
    # Generate dynamic values
    dynamic_event_id = int(base_api.generate_event_id())
    dynamic_session_id = base_api.generate_session_id()
    
    # Create the message body with dynamic values
    message_json_body = {
  "title": f"Send update {random.randint(1, 1000)}",
  "body": "This is a send update body",
  "sms": False,
  "email": False,
  "is_broadcast": True,
  "app_not": True,
  "time_zone": "",
  "attachment_objects": [
    {
      "file_size": "3 MB",
      "file_name": "logo_light.png",
      "url": "https://example.com/logo.png"
    }
  ],
  "selected_ids": [
  ],
  "selected_type": "users",
  "notification_type": "now",
  "time": "18:30",
  "date": "2025-05-22",
  "event_id": dynamic_event_id,
  "audience": {
    "users": {
      "date": "",
      "selected_ids": [],
      "unselected_ids": [],
      "is_select_all": False
    },
    "sessions": {
      "date": "",
      "selected_ids": [int(dynamic_session_id)] if str(dynamic_session_id).isdigit() else [],
      "unselected_ids": [],
      "is_select_all": False
    },
    "groups": {
      "date": "",
      "selected_ids": [],
      "unselected_ids": [],
      "is_select_all": False
    },
    "activities": {
      "date": "",
      "selected_ids": [],
      "unselected_ids": [],
      "is_select_all": False
    },
    "stays": {
      "date": "",
      "selected_ids": [],
      "unselected_ids": [],
      "is_select_all": False
    },
    "flights": {
      "date": "",
      "selected_ids": [],
      "unselected_ids": [],
      "is_select_all": False
    },
    "rides": {
      "date": "",
      "selected_ids": [],
      "unselected_ids": [],
      "is_select_all": False
    },
    "tags": {
      "date": "",
      "selected_ids": [],
      "unselected_ids": [],
      "is_select_all": False
    }
  }
}
    
    return json.dumps(message_json_body)

def get_endpoint():
    # Add event_id as a query parameter
    event_id = base_api.generate_event_id()
    return f"/api/v3/mobile-logistics/home/notification-updates?event_id={event_id}"

def get_method():
    return "POST"

def get_headers():
    return base_api.headers 