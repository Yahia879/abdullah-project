import json
from apis import base_api

def get_notifications_endpoint():
    event_id = base_api.generate_event_id()
    return f"/api/v3/mobile-logistics/notifications/event-list?is_seen=false&event_id={event_id}" #randomize is_seen

def get_staff_access_endpoint():
    event_id = base_api.generate_event_id()
    return f"/api/v3/mobile-logistics/staff-member-access/refresh?event_id={event_id}"

def get_capacity_indicators_endpoint():
    event_id = base_api.generate_event_id()
    return f"/api/v3/mobile-logistics/app-configs/capacity-indicators?event_id={event_id}"

def get_all_events_endpoint(): #Low weight
    limit = 10  
    offset = 0  
    return f"/api/v2/mobile-logistics/all-events-pag?limit={limit}&offset={offset}"

def get_now_up_events_endpoint():
    event_id = base_api.generate_event_id()
    limit = 10  
    offset = 1  
    return f"/api/v3/mobile-logistics/now-up-events?event_id={event_id}&limit={limit}&offset={offset}"

def get_statistics_endpoint():
    event_id = base_api.generate_event_id()
    return f"/api/v3/mobile-logistics/home/statistics?event_id={event_id}"

def get_guests_summary_endpoint():
    event_id = base_api.generate_event_id()
    return f"/api/v3/mobile-logistics/oraganizer-guests-summary?event_id={event_id}"

def get_method():
    return "GET"

def get_headers():
    return base_api.headers 