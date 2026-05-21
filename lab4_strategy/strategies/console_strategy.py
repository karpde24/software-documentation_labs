import json


class ConsoleOutputStrategy:
    def output(self, data):
        print(json.dumps(data, indent=4, ensure_ascii=False))
        return "Data was printed to console"