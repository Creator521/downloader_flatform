import os
import random
import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)

class ProxyManager:
    def __init__(self, proxy_file: str = "proxies.txt", cookie_file: str = "cookies.txt"):
        self.proxy_file = proxy_file
        self.cookie_file = cookie_file
        self.proxies = []
        self.proxy_failures = {}
        self._proxy_index = 0
        self.load_proxies()

    def load_proxies(self):
        """Loads proxies from the file into memory."""
        if os.path.exists(self.proxy_file):
            with open(self.proxy_file, "r") as f:
                # Filter out empty lines and comments
                self.proxies = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        else:
            logger.warning(f"Proxy file {self.proxy_file} not found.")

    def _prune_failed_proxies(self):
        now = time.time()
        self.proxy_failures = {proxy: expires for proxy, expires in self.proxy_failures.items() if expires > now}

    def get_proxy(self) -> Optional[str]:
        """Pick a healthy proxy with a simple round-robin strategy and cooldown."""
        if not self.proxies:
            return None

        self._prune_failed_proxies()
        available = [p for p in self.proxies if p not in self.proxy_failures]
        if not available:
            available = self.proxies

        proxy = available[self._proxy_index % len(available)]
        self._proxy_index = (self._proxy_index + 1) % len(available)
        return proxy

    def mark_proxy_failed(self, proxy: str, cooldown_seconds: int = 120):
        if not proxy:
            return
        self.proxy_failures[proxy] = time.time() + cooldown_seconds

    def clear_proxy_failure(self, proxy: str):
        self.proxy_failures.pop(proxy, None)

    def get_cookie_file(self) -> Optional[str]:
        """Returns the path to the cookie file if it exists and is not empty."""
        try:
            if os.path.exists(self.cookie_file) and os.path.getsize(self.cookie_file) > 10:
                return self.cookie_file
        except OSError:
            pass
        return None

# Global instance
proxy_manager = ProxyManager()
