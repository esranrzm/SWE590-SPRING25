from locust import HttpUser, task, between

class WebUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def load_test(self):
        self.client.get("/")