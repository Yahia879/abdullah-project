import json
import logging
import random
import urllib.parse
import time
import os
from locust import HttpUser, task, TaskSet, between

# Set up logging configuration


# Cache for attendee data 
ATTENDEE_DATA = None

# Authorization headers to use in all requests
HEADERS = {
    "User-Agent": "Load test",
    "Authorization": "Bearer eyJhbGciOiJSUzUxMiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzLUJqMGJDcEhqakJnTGhuUFE1cldENmF6SkNNOVFSUGxYX05OcVNSRGpJIn0.eyJleHAiOjE3NDg2NDI2MDMsImlhdCI6MTc0ODUzNDYwNCwiYXV0aF90aW1lIjoxNzQ4NTM0NjAzLCJqdGkiOiJjOWU3M2M1My0xOTZjLTQyZGYtOWFmMC1hNGMxM2Q0YWM2NmYiLCJpc3MiOiJodHRwczovL2Rldi1pZC5ibGluay5nbG9iYWwvcmVhbG1zL2JsaW5rLWlkIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjgwOTliZGYyLTIzYWUtNDI0Zi05NGY3LTkzMmY1Yjc1MWNhMCIsInR5cCI6IkJlYXJlciIsImF6cCI6ImJhZGdlIiwic2lkIjoiNWFkOTIzOWEtN2Y3OS00YWYyLTg3NzktNjEzNjEyZTAyNmZmIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL2JsaW5rLXNob3AudmVyY2VsLmFwcC8iLCJodHRwOi8vbG9jYWxob3N0OjMwMDAvKiIsImh0dHBzOi8vYWRkLWNhY2hpbmcuZDN1MXlwa2NhcWx1YS5hbXBsaWZ5YXBwLmNvbS8iLCJodHRwczovL2Rldi1zaG9wLmJsaW5rLmdsb2JhbC8iLCJodHRwOi8vbG9jYWxob3N0IiwiaHR0cDovL2xvY2FsaG9zdDozMDAwLyIsImh0dHBzOi8vYWRkLWNhY2hpbmcuZDN1MXlwa2NhcWx1YS5hbXBsaWZ5YXBwLmNvbS8qIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIiwiZGVmYXVsdC1yb2xlcy1ibGluayBpZCJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsImRlbGV0ZS1hY2NvdW50Iiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBjb2duaXRvOmdyb3VwcyIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdXRoX3RpbWUiOjE3NDg1MzQ2MDMsIm5hbWUiOiJNQXJ3YW4gR2FiciIsInByZWZlcnJlZF91c2VybmFtZSI6Im1nYWJyQGJsaW5rLmdsb2JhbCIsImdpdmVuX25hbWUiOiJNQXJ3YW4iLCJmYW1pbHlfbmFtZSI6IkdhYnIiLCJlbWFpbCI6Im1nYWJyQGJsaW5rLmdsb2JhbCJ9.ixFZ2NHQO2IFt_ZuU2jDD5qTe4z-qW7GPHyExVoqlOcWir4x9FmMunA7EFHKrP1SnMT4lUZ_aC_QadTH-tGGP0Jei3HRwI-rD9u8T3tBtG6KfFeXtuUocUJuBnb-uKoJHt4kQHHXqG7T7hnXtfD7I0BLM7wxj89vIYf_NnxENyDDexoo6h2GAwNotc-VcV3I7HCFiDPumQZeSjqHgD5wAJiS7H0Bp-ila0tIEpwRPKcj3gKBqmUTTaJmhXWBhIS5SkV6FCDxnT23n8BUTgX8N5-4me6xCRwAfro5IhLaUmZm336KaLgX089RH9V5zYzFpa0OlOikJJAS86YVFcsRHg",
    "Origin": "blink.global"
}

def load_attendee_data(filename="attendees.json"):
    """Load attendee data from JSON file once and cache it"""
    global ATTENDEE_DATA
    
    if ATTENDEE_DATA is not None:
        return ATTENDEE_DATA
    
    try:
        print(f"Loading attendees from {filename}...")
        start_time = time.time()
        with open(filename, 'r') as f:
            ATTENDEE_DATA = json.load(f)
        load_time = time.time() - start_time
        print(f"Loaded {len(ATTENDEE_DATA)} attendees in {load_time:.2f} seconds")
        
        # Extract and cache unique values for each filter field
        extract_unique_values()
        return ATTENDEE_DATA
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading attendee data: {e}")
        # Return empty list as fallback
        ATTENDEE_DATA = []
        return ATTENDEE_DATA

# Cache for unique values
UNIQUE_VALUES = {
    "industries": [],
    "country": []
}

def extract_unique_values():
    """Extract unique values for each field from the attendee data"""
    global UNIQUE_VALUES
    
    if not ATTENDEE_DATA:
        return
    
    # Print a sample attendee to verify field names
    if ATTENDEE_DATA:
        print("\nSample attendee data for field verification:")
        sample = ATTENDEE_DATA[0]
        for key, value in sample.items():
            if key in ["industryId", "country"]:
                print(f"  {key}: {value}")
    
    # Map JSON field names to our filter field names
    field_mapping = {
        "industries": "industryId",
        "country": "country"
    }
    
    # Extract unique values for each field
    for field, json_field in field_mapping.items():
        unique_values = set()
        for attendee in ATTENDEE_DATA:
            value = attendee.get(json_field)
            if value and isinstance(value, (str, int)) and value != "":
                unique_values.add(value)
        
        # Convert to list and store
        UNIQUE_VALUES[field] = list(unique_values)
        print(f"Extracted {len(UNIQUE_VALUES[field])} unique values for {field}")

class ApiTasksGet(TaskSet):
    def __init__(self, parent):
        super(ApiTasksGet, self).__init__(parent)
        # Load attendee data when class is initialized
        load_attendee_data("resources/attendees.json")

    endpoint = "/api/v3/ga-app/attendees-list"

    @task
    def call_api(self):
        # Define possible filter fields - ONLY organization and country
        filter_fields = ["industries", "country"]
        order_values = ["asc"]
        
        # Create different query parameter combinations
        query_params = [
            # self.create_query_params(filter_fields, order_values, 1),  # Single filter
            # self.create_query_params(filter_fields, order_values, 2),  # Both filters
            self.create_query_params(filter_fields, order_values, 0),  # No filters, just sort
        ]

        # Send each query sequentially
        for i, params in enumerate(query_params):
            # Determine the request name based on filter count
            if i == 0:
                request_name = "Attendees List"
            elif i == 1:
                request_name = "Attendees List - Both Filters"
            else:
                request_name = "Attendees List - No Filters"
                
            # Build the URL with query params
            query_string = urllib.parse.urlencode(params, doseq=True)
            url = f"{self.endpoint}?{query_string}"
            
            # Send the GET request with headers and name
            response = self.client.get(url, headers=HEADERS, name=request_name)

    def create_query_params(self, filter_fields, order_values, num_filters):
        """Create query parameters using real values from attendee data"""
        params = {}
        
        # Always add event_id parameter (static value of 3)
        params["event_id"] = "112"
        
        # Track which fields are being filtered for sorting
        used_filter_fields = []
        
        # Add filters if needed
        if num_filters > 0:
            # Select random fields to filter by
            selected_fields = random.sample(filter_fields, num_filters)
            used_filter_fields = selected_fields
            
            for field in selected_fields:
                # Get a random real value for this field
                if UNIQUE_VALUES[field]:
                    value = random.choice(UNIQUE_VALUES[field])
                    params[f"filter[{field}]"] = value
        
        # Add sort_by parameter - Only sort on fields used for filtering
        # If no filters used, use a random filter field
        if used_filter_fields:
            sort_field = random.choice(used_filter_fields)
        else:
            sort_field = random.choice(filter_fields)
            
        params["sort_by"] = sort_field
        
        # Add order parameter
        params["order"] = random.choice(order_values)
        
        return params

class APILoadTestGet(HttpUser):
    wait_time = between(1, 3)
    tasks = [ApiTasksGet]
    host = "https://loadtest-foundation-api-ga.blink.global"
    
    def on_start(self):
        # Ensure data is loaded when the test starts
        load_attendee_data("resources/attendees.json")

if __name__ == "__main__":
    # For testing outside of Locust
    data = load_attendee_data("resources/attendees.json")
    
    # Create example queries manually without using TaskSet
    filter_fields = ["industries", "country"]
    order_values = ["asc", "desc"]
    endpoint = "/api/v3/ga-app/attendees-list"
    
    print(f"Authorization headers that will be used: {HEADERS}")
    
    # Helper function for standalone testing
    def create_test_params(filter_fields, order_values, num_filters):
        """Create query parameters using real values from attendee data"""
        params = {}
        
        # Always add event_id parameter (static value of 3)
        params["event_id"] = "112"
        
        # Track which fields are being filtered for sorting
        used_filter_fields = []
        
        # Add filters if needed
        if num_filters > 0:
            # Select random fields to filter by
            selected_fields = random.sample(filter_fields, min(num_filters, len(filter_fields)))
            used_filter_fields = selected_fields
            
            for field in selected_fields:
                # Get a random real value for this field
                if UNIQUE_VALUES[field]:
                    value = random.choice(UNIQUE_VALUES[field])
                    params[f"filter[{field}]"] = value
        
        # Add sort_by parameter - Only sort on fields used for filtering
        # If no filters used, use a random filter field
        if used_filter_fields:
            sort_field = random.choice(used_filter_fields)
        else:
            sort_field = random.choice(filter_fields)
            
        params["sort_by"] = sort_field
        
        # Add order parameter
        params["order"] = random.choice(order_values)
        
        return params
    
    # Generate sample queries
    print("\nExample queries that would be made in the load test:")
    for i in range(5):
        # Only use 0, 1, or 2 filters
        num_filters = random.randint(0, 2)
        params = create_test_params(filter_fields, order_values, num_filters)
        query_string = urllib.parse.urlencode(params, doseq=True)
        print(f"\nExample query {i+1}:")
        print(f"  {endpoint}?{query_string}")
        for key, value in params.items():
            print(f"    {key}: {value}")
            
    print("\nUnique filter values found in the data:")
    for field, values in UNIQUE_VALUES.items():
        print(f"  {field}: {values}")
        
    print("\nTo run the load test use: locust -f attendees_list.py")