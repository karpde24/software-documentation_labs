import json
import os


class FileOutputStrategy:
    def __init__(self, file_path):
        self.file_path = file_path

    def output(self, data):
        directory = os.path.dirname(self.file_path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"Data was written to file: {self.file_path}")
