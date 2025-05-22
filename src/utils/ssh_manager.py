import paramiko
import yaml
import os
import re

class SSHManager:
    def __init__(self, config=None):
        self.vms = {}
        self.config = config
        self.vms_file = os.path.join(os.path.dirname(__file__), 'vms.yaml')
        self.load_vms()

    def create_vm(self, name, ip_address, username, password_or_key_path, key_type=None):
        if not self.is_valid_ipv4(ip_address):
            raise ValueError("Invalid IPv4 address format.")
        self.vms[name] = {
            'ip_address': ip_address,
            'username': username,
            'password_or_key_path': password_or_key_path,
            'key_type': key_type
        }
        self.save_vms()

    def is_valid_ipv4(self, ip):
        pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if pattern.match(ip):
            return all(0 <= int(num) <= 255 for num in ip.split('.'))
        return False

    def save_vms(self):
        with open(self.vms_file, 'w') as file:
            yaml.dump(self.vms, file)

    def load_vms(self):
        try:
            with open(self.vms_file, 'r') as file:
                self.vms = yaml.safe_load(file) or {}
        except FileNotFoundError:
            self.vms = {}

    def list_vms(self):
        return self.vms

    def edit_vm(self, name, ip_address=None, username=None, password_or_key_path=None, key_type=None):
        if name in self.vms:
            if ip_address:
                self.vms[name]['ip_address'] = ip_address
            if username:
                self.vms[name]['username'] = username
            if password_or_key_path:
                self.vms[name]['password_or_key_path'] = password_or_key_path
            if key_type:
                self.vms[name]['key_type'] = key_type
            self.save_vms()
        else:
            print(f"VM {name} not found.")

    def delete_vm(self, name):
        if name in self.vms:
            del self.vms[name]
            self.save_vms()
            print(f"VM {name} deleted successfully.")
        else:
            print(f"VM {name} not found.")

    def connect_to_vm(self, ip_address, username, password_or_key_path, key_type=None):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            print(f"Connecting to {ip_address} as {username}...")
            if key_type in ['pem', 'rsa', 'dsa', 'ed25519']:
                password_or_key_path = os.path.expanduser(password_or_key_path)
                print(f"Using key file: {password_or_key_path}")
                
                # Check for case-insensitive match
                dir_name, file_name = os.path.split(password_or_key_path)
                if not dir_name:
                    dir_name = '.'
                print(f"Directory: {dir_name}, File: {file_name}")
                
                # Debugging: List contents of the directory
                print(f"Contents of {dir_name}: {os.listdir(dir_name)}")
                
                # Check if the file exists in a case-insensitive manner
                if not any(f.lower() == file_name.lower() for f in os.listdir(dir_name)):
                    raise FileNotFoundError(f"Key file not found: {password_or_key_path}")
                
                # Check if the file is readable
                if not os.access(password_or_key_path, os.R_OK):
                    print(f"File permissions: {oct(os.stat(password_or_key_path).st_mode)}")
                    raise PermissionError(f"Key file is not readable: {password_or_key_path}")
                
                # Connect using the appropriate key type
                if key_type == 'pem':
                    client.connect(ip_address, username=username, key_filename=password_or_key_path)
                elif key_type == 'rsa':
                    key = paramiko.RSAKey(filename=password_or_key_path)
                    client.connect(ip_address, username=username, pkey=key)
                elif key_type == 'dsa':
                    key = paramiko.DSSKey(filename=password_or_key_path)
                    client.connect(ip_address, username=username, pkey=key)
                elif key_type == 'ed25519':
                    key = paramiko.Ed25519Key(filename=password_or_key_path)
                    client.connect(ip_address, username=username, pkey=key)
            else:
                client.connect(ip_address, username=username, password=password_or_key_path)
            print("Connection established.")
            return client
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials.")
        except paramiko.SSHException as sshException:
            print(f"Unable to establish SSH connection: {sshException}")
        except paramiko.BadHostKeyException as badHostKeyException:
            print(f"Unable to verify server's host key: {badHostKeyException}")
        except FileNotFoundError as fnfError:
            print(fnfError)
        except PermissionError as permError:
            print(permError)
        except Exception as e:
            print(f"Operation error: {e}")
        return None