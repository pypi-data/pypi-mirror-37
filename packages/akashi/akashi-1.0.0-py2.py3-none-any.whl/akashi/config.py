import os
import json
from pathlib import Path

class Config:
    def __init__(self):
        self._config_file = os.path.join(str(Path.home()), ".akashi.json")
    
    def set(self, data={}):
        with open(self._config_file, 'w') as f:
            json.dump(data, f)
    
    def get(self):
        data = None
        if os.path.isfile(self._config_file):
            with open(self._config_file, 'r') as f:
                data = json.load(f)
        return data

    def delete(self):
        result = False
        if os.path.isfile(self._config_file):
            os.remove(self._config_file)
            result = True
        return result
