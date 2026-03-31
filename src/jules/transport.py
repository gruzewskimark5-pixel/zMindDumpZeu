import json
from typing import Dict, Any, Optional
from urllib import request, error

class HttpTransport:
    def __init__(self, baseurl: str, auth):
        self.baseurl = baseurl.rstrip("/")
        self.auth = auth

    def request(self, method: str, path: str, json_payload: Optional[Any] = None) -> Dict[str, Any]:
        url = f"{self.baseurl}/{path.lstrip('/')}"
        data = json.dumps(json_payload).encode("utf-8") if json_payload is not None else None

        req = request.Request(url, data=data, method=method)
        headers = self.auth.apply({"Accept": "application/json"})
        for k, v in headers.items():
            req.add_header(k, v)

        if data:
            req.add_header("Content-Type", "application/json")

        try:
            with request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as e:
            # Simplified error handling to match user style
            body = e.read().decode("utf-8")
            raise Exception(f"API Error {e.code}: {body or e.reason}")
        except Exception as e:
            raise Exception(f"Transport failure: {str(e)}")
