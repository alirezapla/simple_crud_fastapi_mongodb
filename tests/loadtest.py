from locust import TaskSet, constant, task, HttpUser, SequentialTaskSet


class GetQueries(TaskSet):
    @task
    def get_users(self):
        x = self.client.get("/product/")
        print(x)


class MyLoadTest(HttpUser):
    host = "http://web:8080"
    tasks = [GetQueries]
    # wait_time = constant(0.5)
