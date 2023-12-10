from os import environ as env

JITTER_MAX_RETRIES = int(env.get("JITTER_MAX_RETRIES", "10"))
JITTER_RETRY_BACKOFF = bool(int(env.get("JITTER_RETRY_BACKOFF", "1")))
JITTER_RETRY_BACKOFF_MAX = int(env.get("JITTER_RETRY_BACKOFF_MAX", "500"))
JITTER_RETRY_JITTER = bool(int(env.get("JITTER_RETRY_JITTER", "0")))

METHOD_CHOICES = [
    ("GET", "GET"),
    ("POST", "POST"),
    ("PATCH", "PATCH"),
    ("PUT", "PUT"),
    ("OPTIONS", "OPTIONS"),
    ("HEAD", "HEAD"),
    ("DELETE", "DELETE"),
    ("TRACE", "TRACE"),
    ("CONNECT", "CONNECT"),
]
