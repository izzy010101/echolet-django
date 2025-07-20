# Requests per second under sustained load
# pip install locust
# locust -f locustfile.py

from locust import HttpUser, task

class WebsiteUser(HttpUser):
    @task
    def get_home(self):
        self.client.get("/")

    @task
    def get_blog(self):
        self.client.get("/blog/")

    @task
    def get_categories(self):
        self.client.get("/categories/")

    @task
    def get_contact(self):
        self.client.get("/contact/")

    @task
    def get_contact(self):
        self.client.get("/contact/")

    @task
    def get_login(self):
        self.client.get("/login/")

    @task
    def get_register(self):
        self.client.get("/register/")