import subprocess
import sys

def install_setuptools():
    try:
        import setuptools
    except ImportError:
        print("setuptools not found, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools"])
        print("setuptools installed successfully.")

install_setuptools()

from setuptools import setup, find_packages

def install_dependencies():
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")

print("Starting setup for SSH Portal...")

install_dependencies()

setup(
    name='SSH Portal',
    version='0.1.0',
    author='Petr Gallus',
    author_email='gallus-petr@pm.me',
    description='A tool for managing and connecting to virtual machines via SSH.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'paramiko',
        'PyYAML',
    ],
    entry_points={
        'console_scripts': [
            'ssh-portal=main:main',
        ],
    },
)

print("Setup completed successfully.")