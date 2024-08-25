# 2FA Manager

## Overview

2FA Manager is a simple and user-friendly two-factor authentication (2FA) code manager built with Python and Tkinter. The application supports adding, editing, deleting, and viewing OTP (One-Time Password) codes for various services. It automatically refreshes OTP codes every 30 seconds and adapts to the system's dark mode.

## Features

- Add, edit, and delete services.
- Automatically refresh OTP codes with a 30-second countdown.
- Adapts to system dark mode on macOS.
- Simple and intuitive UI with support for both dark and light themes.
- Easily clone and set up the project locally.

## Installation

### Prerequisites

- Python 3.11 or later.
- `pip` (Python package installer).


### Clone the Repository

```bash
git clone https://github.com/yourusername/2fa_manager.git
cd 2fa_manager
```

### Set Up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use 
```

### Install the Requirements

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python run_app.py
```

## Usage

1. **Add a Service**: Click on the "+" button to add a new service. Enter the service name and OTP URI.
2. **Edit a Service**: Click on the three dots next to a service and select "Edit".
3. **Delete a Service**: Click on the three dots next to a service and select "Delete".
4. **View OTP Code**: The OTP code for each service is displayed and automatically refreshes every 30 seconds.

## Unit Testing

Unit tests are provided to ensure the correctness of the core functionality.

### Run Unit Tests

```bash
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any changes you'd like to make.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Thanks to the open-source community for the tools and libraries used in this project.
