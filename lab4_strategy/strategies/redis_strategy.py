import json


class RedisOutputStrategy:
    def __init__(self, host, port, key):
        self.host = host
        self.port = port
        self.key = key

    def output(self, data):
        import redis

        client = redis.Redis(
            host=self.host,
            port=self.port,
            decode_responses=True
        )

        client.set(self.key, json.dumps(data, ensure_ascii=False))

        print(f"Data was written to Redis with key: {self.key}")
