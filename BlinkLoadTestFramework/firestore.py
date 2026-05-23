from locust import FastHttpUser, task, between
import json


class DirectApiTest(FastHttpUser):
    """
    Load test that only calls the API endpoint with a manually provided token
    No login step is performed - you must provide a valid token
    """
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    # API configuration - using empty host as we'll use absolute URL
    host = ""
    
    # Target API configuration 
    api_host = "https://loadtest-foundation-api-ga.blink.global"
    api_endpoint = "/api/v3/ga-app/firebase-email-data"
    
    # REPLACE THIS with your actual access token
    manual_token = "eyJhbGciOiJSUzUxMiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzLUJqMGJDcEhqakJnTGhuUFE1cldENmF6SkNNOVFSUGxYX05OcVNSRGpJIn0.eyJleHAiOjE3NjMwNTg3NTAsImlhdCI6MTc0NzUwNjc1MCwianRpIjoiZGFjNDRlZDAtZGIyOC00NmJmLTgxZmItZTI2OWZjNTE1ZjhlIiwiaXNzIjoiaHR0cHM6Ly9kZXYtaWQuYmxpbmsuZ2xvYmFsL3JlYWxtcy9ibGluay1pZCIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiI1ODY0Y2QxNS0xMWNkLTRlMDQtODAwOC1kZjM4ODY2NmFiYTEiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJiYWRnZSIsInNpZCI6Ijk1ZjNiMmI3LTJhYmMtNDU1Ni1iZDE2LWRiY2M0MzBmZTMwZSIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cDovL2xvY2FsaG9zdDozMDAwLyoiLCJodHRwczovL2FkZC1jYWNoaW5nLmQzdTF5cGtjYXFsdWEuYW1wbGlmeWFwcC5jb20vIiwiaHR0cHM6Ly9kZXYtc2hvcC5ibGluay5nbG9iYWwvIiwiaHR0cDovL2xvY2FsaG9zdCIsImh0dHA6Ly9sb2NhbGhvc3Q6MzAwMC8iLCJodHRwczovL2FkZC1jYWNoaW5nLmQzdTF5cGtjYXFsdWEuYW1wbGlmeWFwcC5jb20vKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtYmxpbmsgaWQiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJkZWxldGUtYWNjb3VudCIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCBjb2duaXRvOmdyb3VwcyIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdXRoX3RpbWUiOjE3NDc1MDY3NTAsIm5hbWUiOiJpUGVPeWUgS21JUVRpIiwicHJlZmVycmVkX3VzZXJuYW1lIjoicW52c2Rnc3EiLCJnaXZlbl9uYW1lIjoiaVBlT3llIiwiZmFtaWx5X25hbWUiOiJLbUlRVGkiLCJlbWFpbCI6ImxvYWR0ZXN0K3FudnNkZ3NxQG54dC5zbyJ9.KoRPZB587FKLzMREMtr_LJJL2TPj4To_bGTw9IfmXkP4foJXhDbBCgJRRoaIkfjP6CWk726toeuHaEVnDPvOqBG9YD7Zw8Ok9Q1ImyCSWEUAedMji0EL3_rN_5Ixv7fMNQ39eauk_8uexI01vUUQSyQEcpYS26CfBkg6JbkJo-lOkhCCJ7CT5vlf75kCke8sGx4D7YmpDMfgamaTwXVFefl4v71ZexudLrxEYXXMEITpECR97-dqoJzTU23gwFDT7ZBUSKKAQ088U3ALncezZtayHpGpbWeXeGmY07PgXP5nov_zv7LNXlGpZMTsxYd56cb26CVDaoe_N9hbP5Om2w"
    
    def on_start(self):
        """
        Initialize the user for the load test
        """
        # Set up headers for the API call
        self.api_headers = {
            "Content-Type": "application/json",
            "User-Agent": "Load Test - Direct API",
            "Origin": "blink.global",
            "Authorization": f"Bearer {self.manual_token}"
        }
    
    @task
    def call_api_directly(self):
        """
        Directly call the API with the manually provided token
        """
        # Construct the full URL
        api_url = f"{self.api_host}{self.api_endpoint}"
        
        # Make the API call using an absolute URL
        with self.client.get(
            url=api_url,
            headers=self.api_headers,
            name="Direct API Call",
            catch_response=True
        ) as api_response:
            if api_response.status_code != 200:
                api_response.failure(f"API call failed with status code: {api_response.status_code}")
                # You can uncomment the following lines to see error details
                # if hasattr(api_response, 'text'):
                #     print(f"Error response: {api_response.text[:300]}")
            else:
                # Success handling - can be customized as needed
                pass 