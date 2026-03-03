import os
import random
from typing import Optional

class ProxyManager:
    def __init__(self, proxy_file: str = "proxies.txt", cookie_file: str = "cookies.txt"):
        self.proxy_file = proxy_file
        self.cookie_file = cookie_file
        self.proxies = []
        self.load_proxies()

    def load_proxies(self):
        """Loads proxies from the file into memory."""
        if os.path.exists(self.proxy_file):
            with open(self.proxy_file, "r") as f:
                # Filter out empty lines and comments
                self.proxies = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        else:
            print(f"Warning: Proxy file {self.proxy_file} not found.")

    def get_proxy(self) -> Optional[str]:
        """Returns a random proxy from the list, or None if no proxies are available."""
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    def get_cookie_file(self) -> Optional[str]:
        """Returns the path to the cookie file if it exists."""
        if os.path.exists(self.cookie_file):
            return self.cookie_file
        print(f"Warning: Cookie file {self.cookie_file} not found.")
        return None

# Global instance
proxy_manager = ProxyManager()
