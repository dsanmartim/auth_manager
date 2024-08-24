from setuptools import find_packages, setup

setup(
    name="2fa_manager",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pyotp",
    ],
    entry_points={
        "console_scripts": [
            "2fa-manager = 2fa_manager.gui:OTPApp",
        ],
    },
)
