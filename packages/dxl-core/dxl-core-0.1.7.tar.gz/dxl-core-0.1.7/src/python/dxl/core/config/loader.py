import json
import yaml
from typing import Dict, Any

def load_config(path: str) -> Dict[str, Any]:
    with open(path) as fin:
        if path.endswith('.yml') or path.endswith('.yaml'):
            return yaml.load(fin)
        if path.endswith('.json'):
            return json.load(fin)
