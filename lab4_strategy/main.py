import json

from data_reader import RevenueBudgetReader
from output_context import OutputContext

from strategies.console_strategy import ConsoleOutputStrategy
from strategies.file_strategy import FileOutputStrategy
from strategies.redis_strategy import RedisOutputStrategy
from strategies.kafka_strategy import KafkaOutputStrategy


def load_config():
    with open("config.json", "r", encoding="utf-8-sig") as file:
        return json.load(file)


def create_strategy(config):
    strategy_name = config["output_strategy"]

    if strategy_name == "console":
        return ConsoleOutputStrategy()

    if strategy_name == "file":
        return FileOutputStrategy(config["output_file"])

    if strategy_name == "redis":
        redis_config = config["redis"]

        return RedisOutputStrategy(
            host=redis_config["host"],
            port=redis_config["port"],
            key=redis_config["key"]
        )

    if strategy_name == "kafka":
        kafka_config = config["kafka"]

        return KafkaOutputStrategy(
            bootstrap_servers=kafka_config["bootstrap_servers"],
            topic=kafka_config["topic"]
        )

    raise ValueError(f"Unknown output strategy: {strategy_name}")


def main():
    config = load_config()

    reader = RevenueBudgetReader(config["dataset_url"])
    data = reader.read_data()

    strategy = create_strategy(config)
    output_context = OutputContext(strategy)

    output_context.execute(data)


if __name__ == "__main__":
    main()
