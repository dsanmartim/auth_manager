import json
import os
import pyotp

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/services.json")


class OTPManager:
    def __init__(self):
        self.services = {}
        self.load_services()

    def load_services(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as file:
                    self.services = json.load(file)
            except json.JSONDecodeError:
                self.services = {}

    def save_services(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.services, file, indent=4)

    def add_service(self, name, uri):
        """Add a new service with the provided name and TOTP URI."""
        self.services[name] = uri
        self.save_services()

    def edit_service(self, old_name, new_name, new_uri):
        """Edit an existing service. If the name changes, the old entry is removed."""
        if old_name in self.services:
            del self.services[old_name]
        self.services[new_name] = new_uri
        self.save_services()

    def delete_service(self, name):
        """Delete a service by its name."""
        if name in self.services:
            del self.services[name]
            self.save_services()

    def get_code(self, name):
        """Generate and return the OTP code for the given service."""
        uri = self.services.get(name)
        if uri:
            try:
                totp = pyotp.parse_uri(uri)
                return totp.now()
            except Exception as e:
                return "Invalid Secret"
        return None
