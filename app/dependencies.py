"""Shared dependencies used across route modules."""
import os
from slowapi import Limiter
from slowapi.util import get_remote_address

# Use Redis for cross-worker rate limiting in production; fall back to in-memory for dev
REDIS_URL = os.getenv("REDIS_URL", "memory://")
limiter = Limiter(key_func=get_remote_address, storage_uri=REDIS_URL)
