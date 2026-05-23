#!/usr/bin/env python3
from locust import HttpUser, task, between, events, TaskSet
import random
import json
import csv
import os
import sys

def load_users_from_csv(csv_path):
    """Load test users from CSV file"""
    users = []
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Cannot proceed with load test.")
        sys.exit(1)
    
    try:
        with open(csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if "email" in row and "password" in row:
                    users.append({
                        "username": row["email"],
                        "password": row["password"]
                    })
        
        if not users:
            print(f"Error: No valid users found in {csv_path}.")
            sys.exit(1)
            
        print(f"Loaded {len(users)} users from {csv_path}")
        return users
        
    except Exception as e:
        print(f"Error loading users from CSV: {str(e)}")
        sys.exit(1)

# Load users at module level to do it only once
csv_path = "resources/users.csv"
all_users = load_users_from_csv(csv_path)

# Hook that runs once on test start
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Print information about the test at startup"""
    print(f"Starting load test with {len(all_users)} users from CSV")

class LoginTaskSet(TaskSet):
    """TaskSet for login operations"""
    
    def on_start(self):
        """Initialize headers for login requests"""
        self.login_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
    
    @task
    def user_login(self):
        """Perform user login using random user from CSV"""
        if not all_users:
            return
            
        # Get a random user
        user = random.choice(all_users)
        
        # Prepare login data
        login_data = {
            "username": user["username"],
            "password": user["password"],
            "client_id": "badge",
            "grant_type": "password"
        }
        
        # Make the login request
        # response_get_ui= self.client.get(
        #     "/realms/blink-id/protocol/openid-connect/auth?client_id=account-console&redirect_uri=https%3A%2F%2Floadtest-id.blink.global%2Frealms%2Fblink-id%2Faccount&state=1ea3fbd8-5821-4344-8fda-f3bd3c610069&response_mode=query&response_type=code&scope=openid&nonce=ae000ff8-5598-4c70-9611-b641957ff314&code_challenge=i-nAjO02aDT3afAPQVMvuZ0MKI4NjZLix5LEOUhlHeQ&code_challenge_method=S256",
        #     name="Get UI"
        # )
        # print(response_get_ui.text)
        response = self.client.post(
            "/realms/blink-id/protocol/openid-connect/token",
            data=login_data, 
            headers=self.login_headers,
            name="User Login"
        )
        
        # Optional: You can add response validation here
        if response.status_code == 200:
            try:
                response_data = response.json()
                access_token = response_data.get("access_token")
                if access_token:
                    # Login successful - token received
                    pass
            except json.JSONDecodeError:
                pass

class LoginLoadTest(HttpUser):
    """Load test for user login process"""
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    tasks = [LoginTaskSet]
    host = "https://loadtest-id.blink.global"
    
    def on_start(self):
        """Ensure users are loaded when the test starts"""
        # Users are already loaded at module level
        pass

if __name__ == "__main__":
    # For testing outside of Locust
    print(f"Loaded {len(all_users)} users for login testing")
    print("To run the load test use: locust -f login_users.py") 