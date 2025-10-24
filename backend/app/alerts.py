
import json
import http.client
from urllib.parse import urlparse
from .settings import SLACK_WEBHOOK

def post_slack(text: str) -> None:
    if not SLACK_WEBHOOK:
        return
    try:
        u = urlparse(SLACK_WEBHOOK)
        conn = http.client.HTTPSConnection(u.netloc, timeout=6)
        payload = json.dumps({"text": text})
        headers = {"Content-Type": "application/json"}
        conn.request("POST", u.path, payload, headers)
        conn.getresponse().read()
        conn.close()
    except Exception:
        # fail silently for demo
        pass
