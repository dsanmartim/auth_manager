import json
import os

import pyotp


class OTPManager:
    def __init__(self, data_file=None):
        self.services = {}
        self.data_file = data_file or os.path.join(
            os.path.dirname(__file__), "../data/services.json"
        )
        self.load_services()

    def load_services(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as file:
                    self.services = json.load(file)
            except json.JSONDecodeError:
                self.services = {}

    def save_services(self):
        with open(self.data_file, "w") as file:
            json.dump(self.services, file, indent=4)

    def add_service(self, name, uri):
        self.services[name] = uri
        self.save_services()

    def edit_service(self, old_name, new_name, new_uri):
        if old_name in self.services:
            del self.services[old_name]
        self.services[new_name] = new_uri
        self.save_services()

    def delete_service(self, name):
        if name in self.services:
            del self.services[name]
            self.save_services()

    def get_code(self, name):
        uri = self.services.get(name)
        if uri:
            totp = pyotp.parse_uri(uri)
            return totp.now()
        return None
