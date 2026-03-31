from dataclasses import dataclass
from typing import Dict

@dataclass
class ApiKeyAuth:
    api_key: str

    def apply(self, headers: Dict[str, str]) -> Dict[str, str]:
        headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
