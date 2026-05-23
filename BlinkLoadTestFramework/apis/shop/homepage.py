import json
from apis import base_api

def get_store_configuration_endpoint():
    event_id = base_api.generate_event_id()
    return f"/api/v1/user/stores/store-configuration?event_id={event_id}"

def get_store_configuration_method():
    return "GET"

def get_check_event_endpoint():
    event_id = base_api.generate_event_id()
    return f"/api/v1/user/stores/check-event-exist?event_id={event_id}"

def get_check_event_method():
    return "GET"

def get_badge_groups_endpoint():
    event_id = base_api.generate_event_id()
    return f"/api/v1/user/badge_groups/badge-groups-summary?event_id={event_id}"

def get_badge_groups_method():
    return "GET"

def get_headers():
    return base_api.headers 