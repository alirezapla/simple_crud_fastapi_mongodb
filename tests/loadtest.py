from locust import TaskSet, constant, task, HttpUser, SequentialTaskSet
import json
import random


class GetQueries(TaskSet):
    # @task
    # def get_users(self):
    #     x = self.client.get("/product/")
    #     if x.status_code != 200:
    #         print(x)
    #     else:
    #         print(x.content)

    @task
    def post_users(self):
        headers = {
            "accept": "application/json",
        }

        json_data = json.dumps(
            {
                "name": f"foo{random.randint(0,10000000)}",
                # "name": "foo",
                "price": 2000.5,
                "description": "product A",
            }
        )
        x = self.client.post("/product/", headers=headers, data=json_data)
        if x.status_code != 200:
            print(x.content)
        else:
            print(x.content)


class MyLoadTest(HttpUser):
    host = "http://web:8080"
    tasks = [GetQueries]
    # wait_time = constant(0.5)
