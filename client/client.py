import json
import os
import time
import urllib.request
from datetime import datetime

# The Service name, resolved by cluster DNS; never an individual Pod IP.
URL = os.environ.get("INVENTORY_URL", "http://inventory:8080/")
INTERVAL = float(os.environ.get("INTERVAL", "1"))

while True:
    stamp = datetime.now().strftime("%H:%M:%S")
    try:
        # urlopen opens a fresh TCP connection each call (no keep-alive),
        # so kube-proxy can pick a different Pod for every request.
        with urllib.request.urlopen(URL, timeout=2) as resp:
            pod = json.load(resp)["pod_name"]
        print(f"{stamp} {resp.status} served by {pod}", flush=True)
    except Exception as exc:
        print(f"{stamp} ERROR {exc}", flush=True)
    time.sleep(INTERVAL)
