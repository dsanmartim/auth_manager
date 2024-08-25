from setuptools import find_packages, setup

setup(
    name="auth_manager",
    version="0.1.0",  # Package version
    author="David Sanmartim",
    author_email="davidsanm@gmail.com",
    description="A 2FA Manager with TOTP support and a countdown timer.",
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["data/services.json"]},
    install_requires=[
        "pyotp",
        "tkinter",
    ],
    entry_points={
        "console_scripts": [
            "auth-manager = auth_manager.gui:OTPApp",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
