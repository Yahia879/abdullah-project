import json
import random
import requests
from apis import base_api

FOUNDATION_HOST = "https://dev-foundation-api-user.blink.global"

_FALLBACK_FORM_IDS = [
    "f83e5f200a50ebb0aa9069ee6d7fba12",
    "047a16ee2ac46ce6f62a35355e7630b0"
]

_form_ids = list(_FALLBACK_FORM_IDS)


def load_form_ids():
    """Fetch valid badge form IDs from the API before the test starts."""
    global _form_ids
    try:
        url = f"{FOUNDATION_HOST}/api/v3/blink-shop/user-badges?event_id=112"
        resp = requests.get(url, headers=base_api.shop_headers, timeout=10)
        if resp.status_code == 200:
            ids = [
                badge["custom_id"]
                for badge in resp.json().get("user_badges", [])
                if badge.get("is_assign_form_enabled") and badge.get("custom_id")
            ]
            if ids:
                _form_ids = ids
                print(f"[Shop] Loaded {len(_form_ids)} badge form IDs from API")
                return
        print(f"[Shop] user-badges returned {resp.status_code}, using fallback IDs")
    except Exception as e:
        print(f"[Shop] Warning: could not fetch form IDs ({e}), using fallback IDs")


def _get_form_id():
    return random.choice(_form_ids)


def get_user_badge_endpoint():
    return f"{FOUNDATION_HOST}/api/v3/blink-shop/assigned-form-details/{_get_form_id()}?event_id=112"

def get_user_badge_method():
    return "GET"

def get_assign_badge_endpoint():
    return f"{FOUNDATION_HOST}/api/v3/blink-shop/assigned-form-details/{_get_form_id()}?event_id=112"

def get_assign_badge_method():
    return "PATCH"

def create_assign_badge_message():
    name = base_api.generate_name()
    parts = name.split(" ", 1)
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ""
    email = base_api.generate_email()

    message = {
        "configuration_obj": {
            "general": {"title": "General", "fields": {}},
            "documents": {"title": "Documents", "fields": {}},
            "other_info": {"title": "Other Info", "fields": {}},
            "address_info": {"title": "Address Info", "fields": {}},
            "contact_info": {
                "title": "Contact Info",
                "fields": {
                    "email": {"value": email},
                    "linkedin_url": {"value": ""},
                    "contact_number": {"value": {"code": "44", "number": str(base_api.generate_numbers())}},
                    "confirmation_email": {"value": email}
                }
            },
            "personal_info": {
                "title": "Personal Info",
                "fields": {
                    "image": {"value": ""},
                    "title": {"value": "Agent"},
                    "last_name": {"value": last_name},
                    "first_name": {"value": first_name},
                    "organization": {"value": base_api.generate_string()}
                }
            },
            "travel_documents": {"title": "Travel Documents", "fields": {}},
            "identification_info": {"title": "Identification Info", "fields": {}}
        }
    }
    return json.dumps(message)

def get_headers():
    return base_api.shop_headers
