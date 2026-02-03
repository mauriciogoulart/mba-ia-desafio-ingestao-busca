import json
import os

class JsonFileReader:
    def read(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)