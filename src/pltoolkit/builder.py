import json
from pathlib import Path
import numpy as np
from datetime import datetime

class Builder:

    def __init__(self, author='pl', number=None, exclude=False, type='measurement'):
        self._data = {}
        self._metadata = {}
        self._metadata['created'] = datetime.now().isoformat()
        self._metadata['author'] = author
        self._metadata['number'] = number
        self._metadata['exclude'] = exclude
        self._metadata['type'] = type

    def save(self, filename):
        """
        Speichert die Daten in einer Datei.
        """
        with open(filename, "w") as f:
            f.write(f"metadata: {json.dumps(self._metadata)}\n")
            for key, value in self._data.items():
                f.write(f"{key}: {value}\n")
    def join(self, directory):
        """
        join all json objects in directory into single json array and save to file
        """
        directory = Path(directory).expanduser().resolve()

        if not directory.exists():
            raise FileNotFoundError(directory)

        json_files = [file for file in directory.iterdir() if file.is_file() and file.suffix == ".json"]

        all_data = []

        for json_file in json_files:
            with open(json_file, "r") as f:
                if json_file.name == "combined.json":
                    continue  # Skip the combined file if it exists
                data = json.load(f)
                if data["metadata"]["exclude"] or data["metadata"]["type"] != "measurement":
                    continue  # Skip excluded files
                all_data.append({data["metadata"]["number"]: data})

        output_file = directory / "combined.json"
        with open(output_file, "w") as f:
            json.dump(all_data, f, indent=4)

        print(f"Combined JSON saved to: {output_file}")