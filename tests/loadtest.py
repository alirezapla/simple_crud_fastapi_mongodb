from locust import TaskSet, constant, task, HttpUser, SequentialTaskSet


class GetQueries(TaskSet):
    @task
    def get_users(self):
        self.client.get("/user/")


class MyLoadTest(HttpUser):
    host = "http://localhost:8080"
    tasks = [GetQueries]
    # wait_time = constant(0.5)
