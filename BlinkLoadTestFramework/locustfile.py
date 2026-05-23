from locust import HttpUser, task, between, events, tag
from apis.base_api import ssoid_list, email_list, headers
from apis.base_api import orgapp_headers, admission_headers, shop_headers, appsync_headers, APPSYNC_TOKEN
import random
import json
import time
import os
import threading
import traceback

# from apis.orgapp import login as orgapp_login, homepage, notification_templates, notification_updates
from apis.orgapp import experiences, sessions, venues, attendees, homepage, notification_templates, notification_updates
from apis.admission import login as admission_login, user_search, qr_code
from apis.shop import login as shop_login, homepage as shop_homepage, badges
from apis.eventapp import appsync
from apis.eventapp import (
    profile_update, attendee_connect, attendee_unconnect, 
    schedule_session, session_unschedule, attendee_fcm_token,
    attendee_interest_update, attendee_update
)

ERROR_LOG_FILE = "error_offset.json"
error_log_lock = threading.Lock()

request_bodies = {}

def initialize_error_log():
    if not os.path.exists(ERROR_LOG_FILE):
        with open(ERROR_LOG_FILE, 'w') as f:
            json.dump([], f)

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    badges.load_form_ids()

# Universal error logger that works with any Locust version
@events.request.add_listener
def log_request_errors(request_type, name, response_time, response_length, exception=None, **kwargs):
    """Log all requests that return 400-599 status codes and all failed requests"""
    # Get response if available
    response = kwargs.get('response', None)
    context = kwargs.get('context', {}) 
    
    # Determine if we should log this request
    should_log = False
    status_code = None
    response_text = None
    
    # Case 1: There was an exception (network error, timeout, etc.)
    if exception:
        should_log = True
    
    # Case 2: Request completed but with an error status code
    elif response and hasattr(response, 'status_code') and 400 <= response.status_code < 600:
        should_log = True
        status_code = response.status_code
        response_text = response.text[:500] if hasattr(response, 'text') and response.text else None
    
    # Skip logging if no error condition was met
    if not should_log:
        return
    
    # Get request body if available
    request_body = None
    request_id = context.get('request_id', None) if context else None
    if request_id and request_id in request_bodies:
        request_body = request_bodies.pop(request_id)  # Remove after use to save memory
    
    # Create error data
    error_data = {
        "timestamp": time.time(),
        "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
        "request_type": request_type,
        "name": name,
        "response_time_ms": round(response_time)
    }
    
    # Add exception details if applicable
    if exception:
        error_data.update({
            "exception": str(exception),
            "stack_trace": traceback.format_exc()
        })
    
    # Add response details if available
    if response:
        if hasattr(response, 'url'):
            error_data["url"] = response.url
        
        if status_code:
            error_data["status_code"] = status_code
        
        if response_text:
            error_data["response_text"] = response_text
    
    # Add request body if available
    if request_body:
        error_data["request_body"] = request_body
    
    # Write to error log file in a thread-safe manner
    with error_log_lock:
        try:
            with open(ERROR_LOG_FILE, 'r') as f:
                errors = json.load(f)
            
            errors.append(error_data)
            
            with open(ERROR_LOG_FILE, 'w') as f:
                json.dump(errors, f, indent=2)
        except Exception as e:
            print(f"Error logging to {ERROR_LOG_FILE}: {e}")

# Track request bodies by adding a hook before the request is sent
@events.request.add_listener
def track_request_body(request_type, name, **kwargs):
    """Store request bodies to correlate with responses later"""
    try:
        # Get request object if available (might not be in newer Locust versions)
        request = kwargs.get('request', None)
        if not request:
            return
            
        # Get or create context
        context = kwargs.get('context', {}) if 'context' in kwargs else {}
        
        # Generate a unique ID for this request
        request_id = id(request)
        context['request_id'] = request_id
        
        # Try to get the request body
        if hasattr(request, 'body') and request.body:
            try:
                body_str = request.body
                if isinstance(body_str, bytes):
                    body_str = body_str.decode('utf-8')
                
                if body_str:
                    try:
                        request_bodies[request_id] = json.loads(body_str)
                    except:
                        request_bodies[request_id] = body_str
            except:
                request_bodies[request_id] = str(request.body)[:1000]  # Limit size
    except Exception as e:
        print(f"Error tracking request body: {e}")

# Initialize error log when module is loaded
initialize_error_log()


# class OrgAppUser(HttpUser):
#     wait_time = between(1, 3)
#     host = "https://dev-foundation-api-ga.blink.global"
    
        
#     def on_start(self):
#         self.headers = orgapp_headers.copy()
        
        
    

#     @task(1)
#     def get_notifications(self):
#         self.client.get(
#             homepage.get_notifications_endpoint(),
#             headers=self.headers,
#             name="Homepage - Get Notifications"
#         )
    
#     @task(1)
#     def get_staff_access(self):
#         self.client.get(
#             homepage.get_staff_access_endpoint(),
#             headers=self.headers,
#             name="Homepage - Get Staff Access"
#         )
    
#     @task(1)
#     def get_capacity_indicators(self):
#         self.client.get(
#             homepage.get_capacity_indicators_endpoint(),
#             headers=self.headers,
#             name="Homepage - Get Capacity Indicators"
#         )
    
#     @task(1)
#     def get_all_events(self):
#         self.client.get(
#             homepage.get_all_events_endpoint(),
#             headers=self.headers,
#             name="Homepage - Get All Events"
#         )
    
#     @task(1)
#     def get_now_up_events(self):
#         self.client.get(
#             homepage.get_now_up_events_endpoint(),
#             headers=self.headers,
#             name="Homepage - Get Now Up Events"
#         )
    
#     @task(1)
#     def get_statistics(self):
#         self.client.get(
#             homepage.get_statistics_endpoint(),
#             headers=self.headers,
#             name="Homepage - Get Statistics"
#         )
    
#     @task(1)
#     def get_guests_summary(self):
#         self.client.get(
#             homepage.get_guests_summary_endpoint(),
#             headers=self.headers,
#             name="Homepage - Get Guests Summary"
#         )
    
    
#     @task(3)
#     def get_notification_templates(self):
#         self.client.get(
#             notification_templates.get_endpoint(),
#             headers=self.headers,
#             name="Notifications - Get Templates"
#         )
    
#     @task(2)
#     def send_notification_update(self):
#         endpoint = notification_updates.get_endpoint()
#         data = notification_updates.create_message()
        
#         self.client.post(
#             endpoint, 
#             data=data, 
#             headers=self.headers,
#             name="Notifications - Send Update"
#         )
    
    
#     @task(6)
#     def get_experiences_stats(self):
#         self.client.get(
#             experiences.get_experiences_stats_endpoint(),
#             headers=self.headers,
#             name="Experiences - Get Stats"
#         )
    
#     @task(4)
#     def post_calendar_activity(self):
#         endpoint = experiences.get_calendar_activity_endpoint()
#         data = experiences.create_calendar_activity_message()
        
#         self.client.post(
#             endpoint, 
#             data=data, 
#             headers=self.headers,
#             name="Experiences - Post Calendar Activity"
#         )
    
    
#     @task(10)
#     def get_sessions(self):
#         self.client.get(
#             sessions.get_sessions_endpoint(),
#             headers=self.headers,
#             name="Sessions - Get Sessions"
#         )
    
#     @task(10)
#     def check_user_access(self):
#         response= self.client.get(
#             sessions.get_check_user_access_endpoint(),
#             headers=self.headers,
#             name="Sessions - Check User Access"
#         )

#         # print(response.text)
        
    
#     @task(5)
#     def checkin(self):
#         response = self.client.patch(
#             sessions.get_checkin_endpoint(),
#             headers=self.headers,
#             name="Sessions - Checkin"
#         )
        
#         # Handle response status codes
#         if response.status_code not in [200, 422]:
#             # Log the error but don't fail the test
#             print(f"Checkin failed with status: {response.status_code}")
    
#     @task(5)
#     def get_session_scan_logs(self):
#         self.client.get(
#             sessions.get_session_scan_logs_endpoint(),
#             headers=self.headers,
#             name="Sessions - Get Scan Logs"
#         )
    
#     @task(5)
#     def get_venues(self):
#         self.client.get(
#             venues.get_venues_endpoint(),
#             headers=self.headers,
#             name="Venues - Get Venues"
#         )
    
#     @task(6)
#     def get_venue_sessions(self):
#         self.client.get(
#             venues.get_venue_sessions_endpoint(),
#             headers=self.headers,
#             name="Venues - Get Venue Sessions"
#         )
    
    
#     @task(1)
#     def get_attendees(self):
#         endpoint = attendees.get_endpoint()
#         data = attendees.create_message()
        
#         self.client.patch(
#             endpoint, 
#             data=data, 
#             headers=self.headers,
#             name="Attendees - Update Attendees"
#         )


# class AdmissionUser(HttpUser):
#     wait_time = between(1, 3)
#     host = "https://dev-foundation-api-admin.blink.global"
    
#     def on_start(self):
#         self.headers = admission_headers.copy()
    
#     @task(5)
#     def search_users(self):
#         self.client.get(
#             user_search.get_endpoint(),
#             headers=self.headers
#         )
    
#     @task(10)
#     def show_item(self):
#         self.client.get(
#             qr_code.get_show_item_endpoint(),
#             headers=self.headers
#         )
    
#     @task(8)
#     def send_verification_code(self):
#         endpoint = qr_code.get_send_verification_endpoint()
#         data = qr_code.create_send_verification_message()
        
#         self.client.post(
#             endpoint, 
#             data=data, 
#             headers=self.headers
#         )
    
#     @task(8)
#     def verify_code(self):
#         endpoint = qr_code.get_verify_code_endpoint()
#         data = qr_code.create_verify_code_message()
        
#         self.client.post(
#             endpoint, 
#             data=data, 
#             headers=self.headers
#         )
    
#     @task(15)
#     def print_admission_item(self):
#         endpoint = qr_code.get_print_endpoint()
#         data = qr_code.create_print_message()
        
#         self.client.patch(
#             endpoint, 
#             data=data, 
#             headers=self.headers
#         )


class ShopUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://dev-shop-api-user.blink.global"
    
    def on_start(self):
        self.headers = shop_headers.copy()
        

#     # @task(1)  # TODO: fix login endpoint
#     # def login_task(self):
#     #     pass

#     @task(10)
#     def get_store_configuration(self):
#         self.client.get(
#             shop_homepage.get_store_configuration_endpoint(),
#             headers=self.headers
#         )

#     @task(8)
#     def check_event_exist(self):
#         self.client.get(
#             shop_homepage.get_check_event_endpoint(),
#             headers=self.headers
#         )

#     @task(7)
#     def get_badge_groups(self):
#         self.client.get(
#             shop_homepage.get_badge_groups_endpoint(),
#             headers=self.headers
#         )

    @task(9)
    def get_user_badge(self):
        self.client.get(
            badges.get_user_badge_endpoint(),
            name="/api/v3/blink-shop/assigned-form-details/[id]",
            headers=self.headers
        )

    # @task(8)  # TODO: upload payload not defined yet
    # def upload_photo(self):
    #     pass

    # @task(15)
    # def assign_badge(self):
    #     endpoint = badges.get_assign_badge_endpoint()
    #     data = badges.create_assign_badge_message()

    #     self.client.patch(
    #         endpoint,
    #         name="/api/v3/blink-shop/assigned-form-details/[id]",
    #         data=data,
    #         headers=self.headers
    #     )


# class EventAppUser(HttpUser):
#     wait_time = between(1, 3)  
#     host = "https://dev-integration.blink.global"

    
#     def on_start(self):
#         self.headers = {
#             "Content-Type": "application/json",
#             "User-Agent": "Load test - EventApp",
#             "Authorization": "Bearer gILwqWSfFoEZhFWG7v+kzLjlYwQKVQl1aWBsfZKsh7s=",
#             "Origin": "blink.global"
#         }
#         self.endpoint = "/gw/publish"
    
#     @task(1)
#     def update_profile(self):
#         json_body = profile_update.create_message_json()
#         self.client.post(
#             self.endpoint,
#             json=json_body,
#             headers=self.headers,
#             name="EventApp-UpdateProfile"  # Custom name for this operation
#         )
    
#     @task(5)
#     def connect_attendees(self):
#         json_body = attendee_connect.create_message_json()
#         self.client.post(
#             self.endpoint,
#             json=json_body,
#             headers=self.headers,
#             name="EventApp-ConnectAttendees"  # Custom name for this operation
#         )
    
#     @task(2)
#     def disconnect_attendees(self):
#         self.client.post(
#             self.endpoint,
#             json=attendee_unconnect.create_message_json(),
#             headers=self.headers,
#             name="EventApp-DisconnectAttendees"  # Custom name for this operation
#         )
    
#     @task(5)
#     def schedule_a_session(self):
#         self.client.post(
#             self.endpoint,
#             json=schedule_session.create_message_json(),
#             headers=self.headers,
#             name="EventApp-ScheduleSession"  # Custom name for this operation
#         )
    
#     @task(2)
#     def unschedule_a_session(self):
#         self.client.post(
#             self.endpoint,
#             json=session_unschedule.create_message_json(),
#             headers=self.headers,
#             name="EventApp-UnscheduleSession"  # Custom name for this operation
#         )
    
#     @task(1)
#     def update_fcm_token(self):
#         self.client.post(
#             self.endpoint,
#             json=attendee_fcm_token.create_message_json(),
#             headers=self.headers,
#             name="EventApp-UpdateFCMToken"  # Custom name for this operation
#         )
    
#     @task(1)
#     def update_interests(self):
#         self.client.post(
#             self.endpoint,
#             json=attendee_interest_update.create_message_json(),
#             headers=self.headers,
#             name="EventApp-UpdateInterests"  # Custom name for this operation
#         )
    
#     @task(1)
#     def update_attendee(self):
#         self.client.post(
#             self.endpoint,
#             json=attendee_update.create_message_json(),
#             headers=self.headers,
#             name="EventApp-UpdateAttendee"  # Custom name for this operation
#         )

# class EventAppSyncUser(HttpUser):
#     wait_time = between(1, 3)  
#     host = ""  # Empty host since we're using absolute URL in appsync.py
    
#     def on_start(self):
#         self.headers = {
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {APPSYNC_TOKEN}",
#         }
#         appsync.set_token(self.headers["Authorization"])
    
#     @task(1)
#     def get_categories(self):
#         data = appsync.create_categories_message()
#         self.client.post(
#             appsync.get_endpoint(),
#             data=data,
#             headers=self.headers,
#             name="GraphQL-Categories"  # Custom name for this operation
#         )
    
#     @task(5)
#     def get_entities(self):
#         self.client.post(
#             appsync.get_endpoint(),
#             data=appsync.create_entities_message(),
#             headers=self.headers,
#             name="GraphQL-Entities"  # Custom name for this operation
#         )
    
#     @task(1)
#     def get_places(self):
#         self.client.post(
#             appsync.get_endpoint(),
#             data=appsync.create_places_message(),
#             headers=self.headers,
#             name="GraphQL-Places"  # Custom name for this operation
#         )
    
#     @task(2)
#     def get_halls(self):
#         self.client.post(
#             appsync.get_endpoint(),
#             data=appsync.create_halls_message(),
#             headers=self.headers,
#             name="GraphQL-Halls"  # Custom name for this operation
#         )
    
#     @task(2)
#     def get_venues(self):
#         self.client.post(
#             appsync.get_endpoint(),
#             data=appsync.create_venues_message(),
#             headers=self.headers,
#             name="GraphQL-Venues"  # Custom name for this operation
#         )
    
#     @task(5)
#     def get_sessions(self):
#         self.client.post(
#             appsync.get_endpoint(),
#             data=appsync.create_sessions_message(),
#             headers=self.headers,
#             name="GraphQL-Sessions"  # Custom name for this operation
#         ) 