import json
import os

host = os.getenv("SERVER_HOST", "0.0.0.0")  # nosec
port = os.getenv("SERVER_PORT", 8080)

# Gunicorn config variables
loglevel = os.getenv("SERVER_LOG_LEVEL", "INFO").lower()
workers = int(os.getenv("SERVER_WORKERS", 1))
bind = f"{host}:{port}"
keepalive = int(os.getenv("SERVER_KEEPALIVE", 5))
timeout = int(os.getenv("SERVER_TIMEOUT", 30))

# For debugging and testing
log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    "keepalive": keepalive,
    "timeout": timeout,
}
print(json.dumps(log_data))
