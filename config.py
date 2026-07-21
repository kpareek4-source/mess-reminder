import os
import json

TOPIC = os.getenv("NTFY_TOPIC")

WHATSAPP_SUBSCRIBERS = json.loads(os.getenv("WHATSAPP_SUBSCRIBERS", "[]"))