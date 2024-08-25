# Auth Manager

## Overview

**Auth Manager** is a simple and intuitive 2FA (Two-Factor Authentication) manager that supports TOTP (Time-based One-Time Password) codes. This tool allows you to manage your TOTP-based 2FA codes in one place, with a user-friendly graphical interface.

## Features

- **TOTP Code Generation**: Generate and display TOTP codes for multiple services.
- **Automatic Refresh**: Codes automatically refresh every 30 seconds, with a countdown timer displayed next to each code.
- **Service Management**: Add, edit, and delete services easily from the interface.
- **Dark Mode Support**: The application adapts to the system's dark mode setting, changing colors accordingly.

## Installation

### Prerequisites

- Python 3.11 or higher
- ``tkinter`` must be installed on your system. It is usually included with Python, but if not, you may need to install it separately:

    - On Debian/Ubuntu-based systems: `sudo apt-get install python3-tk`
    - On RedHat/CentOS-based systems: `sudo yum install python3-tkinter`
    - On macOS, `tkinter` is included with the Python framework.

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/auth_manager.git
    cd auth_manager
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    python run_app.py
    ```

## Usage

1. **Add a New Service**: Click the "+" button at the bottom-right corner of the window to add a new service. Enter the service name and TOTP URI, then click "Save."
2. **Edit a Service**: Click on the three-dot menu next to the service you want to edit, select "Edit," make the necessary changes, and click "Save."
3. **Delete a Service**: Click on the three-dot menu next to the service you want to delete, select "Delete," and confirm the deletion.


## Project Structure

- **auth_manager/**: Contains the core application files ( and ).
- **data/**: Stores the  file, which contains your service data.
- **tests/**: Contains unit tests for the application.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have suggestions for improvements or encounter any bugs.

### Running Tests

Unit tests are provided to verify the functionality of the Auth Manager. 
If you make a contribution, make sure to add unit test to it. 
To run the tests, execute the following command:

```bash
python -m pytest -vs tests/test_manager.py
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Author

**David Sanmartim**
- GitHub: [dsanmartim](https://github.com/dsanmartim)
- Email: [davidsanm@gmail.com](mailto:davidsanm@gmail.com)

