import os
import json
from datetime import datetime


class StorageManager:

    def __init__(self):
        self.results_folder = "results"
        os.makedirs(self.results_folder, exist_ok=True)
        self.results_file = os.path.join(
            self.results_folder,
            "captions.json"
        )

    def save_result(self, filename, caption, image_details):
        data = {
            "filename": filename,
            "caption": caption,
            "image_details": image_details,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        existing_data = self.load_results()
        existing_data.append(data)

        with open(self.results_file, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, indent=4)

        return True

    def load_results(self):
        if not os.path.exists(self.results_file):
            return []

        try:
            with open(self.results_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception:
            return []
