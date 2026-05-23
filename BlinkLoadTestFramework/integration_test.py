import json
import logging

import gevent
from locust import FastHttpUser, task, TaskSet, constant_pacing
from apis.eventapp import profile_update
from apis import base_api


class ApiTasks(TaskSet):
    def __init__(self, parent):
        super(ApiTasks, self).__init__(parent)

    endpoint = "/gw/publish"

    @task
    def call_api(self):
        events = [
            {"body": profile_update.create_message_json()},
            # {"body": attendee_connect.create_message_json()},
            # {"body": attendee_unconnect.create_message_json()},
            # {"body": schedule_session.create_message_json()}
        ]

        
        jobs = []
        for event in events:
            jobs.append(gevent.spawn(self.concurrent_request, event["body"]))
        gevent.joinall(jobs)

    def concurrent_request(self, body):
        body_str = json.dumps(body)
        response = self.client.post(self.endpoint, json=json.loads(body_str), headers=base_api.headers)
        
        
        if response.status_code == 400:
            logging.error("400 Bad Request Response:")
            logging.error("Request Body: %s", response.request.body)
            logging.error("Response Status: %d", response.status_code)
            logging.error("Response Body: %s", response.text)

class APILoadTest(FastHttpUser):
    wait_time = constant_pacing(1/1000)
    tasks = [ApiTasks]