# SSH Portal

SSH Portal is a command-line tool designed to simplify the management and connection to virtual machines (VMs) via SSH. This tool provides an intuitive menu-driven interface for users to create, manage, and connect to VMs with ease.

## Features

- Create new virtual machines.
- Manage existing virtual machines (edit, delete, group).
- Connect to virtual machines using SSH with options for IP address, username, and password or SSH key path.

## Requirements

- Python 3.6+
- `pip` (Python package installer)

## Installation

### Step 1: Clone the Repository

```sh
git clone https://github.com/PetrGallus/ssh-portal.git
cd SSH-Portal
```

### Step 2: Create a Virtual Environment

Create a virtual environment to avoid conflicts with other Python packages.

```sh
python3 -m venv venv
```

### Step 3: Activate the Virtual Environment

Activate the virtual environment.

For Linux/macOS:
```sh
source venv/bin/activate
```

For Windows:
```sh
venv\Scripts\activate
```

### Step 4: Install Dependencies

Install the required dependencies.

```sh
pip install -r requirements.txt
```

### Step 5: Run the Setup Script

Run the setup script to complete the installation.

```sh
python setup.py install
```


## Usage

To start the application, run the following command:

```
python src/main.py
```

Once the application is running, you will be presented with a menu that allows you to:

[1] Create a new VM
[2] Manage existing VMs
[3] Connect to a VM

Follow the prompts to perform the desired actions.

## Configuration

The application uses a configuration file located at `src/config/config.yaml`. You can modify this file to set default SSH parameters and other necessary settings for managing your VMs.

## Dependencies

- paramiko: For SSH connections.
- PyYAML: For parsing YAML configuration files.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.