from locust import HttpUser, task, between, SequentialTaskSet
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UserBehavior(SequentialTaskSet):
    def on_start(self):
        # This method is called when a simulated user starts a test
        self.login()

    def login(self):
        response = self.client.post("/login", json={"username": "test", "password": "password"})
        if response.status_code == 200:
            if "application/json" in response.headers.get("Content-Type", ""):
                try:
                    json_response = response.json()
                    logger.info("Login successful, received data: %s", json_response)
                    self.client.cookies.update(response.cookies)  # If cookies need to be carried over
                except ValueError:
                    logger.error(f"Failed to parse response JSON: {response.text}")
                    logger.debug(f"Response headers: {response.headers}")
                    self.interrupt(reschedule=True)
            else:
                logger.error(f"Unexpected content type: {response.headers.get('Content-Type')}")
                logger.debug(f"Response content: {response.text}")
                self.interrupt(reschedule=True)
        else:
            logger.error(f"Login failed with status code {response.status_code}: {response.text}")
            self.interrupt(reschedule=True)

    @task(2)
    def view_dashboard(self):
        with self.client.get("/dashboard", catch_response=True) as response:
            if response.ok:
                logger.info("Dashboard accessed successfully")
            else:
                logger.error(f"Failed to access dashboard: {response.status_code}")
                logger.debug(f"Response content: {response.text}")
                logger.debug(f"Response headers: {response.headers}")
                response.failure("Dashboard access failed")

    @task(1)
    def post_update(self):
        data = {"status": "Here's a new update!"}
        with self.client.post("/update", json=data, catch_response=True) as response:
            if response.ok:
                logger.info("Update posted successfully")
            else:
                logger.error(f"Failed to post update: {response.status_code}")
                logger.debug(f"Response content: {response.text}")
                logger.debug(f"Response headers: {response.headers}")
                response.failure("Update post failed")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Random wait time between tasks for each user from 1 to 5 seconds
    host = "https://www.flipkart.com"
