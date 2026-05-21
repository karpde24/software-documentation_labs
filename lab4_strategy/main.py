import json

from data_reader import RevenueBudgetReader
from output_context import OutputContext

from strategies.console_strategy import ConsoleOutputStrategy
from strategies.file_strategy import FileOutputStrategy
from strategies.redis_strategy import RedisOutputStrategy
from strategies.kafka_strategy import KafkaOutputStrategy
from strategies.firebase_strategy import FirebaseOutputStrategy


def load_config():
    with open("config.json", "r", encoding="utf-8-sig") as file:
        return json.load(file)


def create_strategy(config, strategy_name=None):
    selected_strategy = strategy_name or config["output_strategy"]

    if selected_strategy == "console":
        return ConsoleOutputStrategy()

    if selected_strategy == "file":
        return FileOutputStrategy(config["output_file"])

    if selected_strategy == "firebase":
        firebase_config = config["firebase"]

        return FirebaseOutputStrategy(
            service_account_file=firebase_config["service_account_file"],
            collection=firebase_config["collection"]
        )

    if selected_strategy == "redis":
        redis_config = config["redis"]

        return RedisOutputStrategy(
            host=redis_config["host"],
            port=redis_config["port"],
            key=redis_config["key"]
        )

    if selected_strategy == "kafka":
        kafka_config = config["kafka"]

        return KafkaOutputStrategy(
            bootstrap_servers=kafka_config["bootstrap_servers"],
            topic=kafka_config["topic"]
        )

    raise ValueError(f"Unknown output strategy: {selected_strategy}")


def run_strategy(strategy_name=None):
    config = load_config()

    reader = RevenueBudgetReader(config["dataset_url"])
    data = reader.read_data()

    strategy = create_strategy(config, strategy_name)
    output_context = OutputContext(strategy)

    result = output_context.execute(data)

    return {
        "strategy": strategy_name or config["output_strategy"],
        "records_count": len(data),
        "result": result or "Strategy executed successfully"
    }


def main():
    result = run_strategy()
    print(result)


if __name__ == "__main__":
    main()