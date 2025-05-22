import readline
import os
import time
import paramiko

def complete_path(text, state):
    return [x for x in os.listdir('.') if x.startswith(text)][state]

readline.set_completer(complete_path)
readline.parse_and_bind("tab: complete")

def print_welcome_banner():
    banner = """
    ==========================================
    |                                         |
    |          Welcome to SSH Portal          |
    |                                         |
    ==========================================
    """
    print(banner)

def print_section_header(title):
    header = f"""
    ==========================================
    |                                         |
    |          {title.center(15)}          |
    |                                         |
    ==========================================
    """
    print(header)

def display_menu(ssh_manager):
    print_welcome_banner()
    print("\n\nPlease choose an option:\n")
    while True:
        print("[1]   Create a new SSH connection")
        print("[2]   Manage existing SSH connections")
        print("[3]   Connect to a machine via SSH")
        print("[4]   Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            create_ssh_connection(ssh_manager)
        elif choice == '2':
            manage_ssh_connections(ssh_manager)
        elif choice == '3':
            connect_to_vm(ssh_manager)
        elif choice == '4':
            print("\nExiting the program...")
            time.sleep(1)
            print("\nGoodbye!\n\n")
            return False
        else:
            print("Invalid choice. Please try again.\n\n\n")

def create_ssh_connection(ssh_manager):
    name = input("Enter Name for your SSH Connection: ")
    while True:
        ip_address = input("Enter IP address: ")
        if ssh_manager.is_valid_ipv4(ip_address):
            break
        else:
            print("Invalid IPv4 address format. Please try again.")
    username = input("Enter username for login: ")
    password_or_key_path = input("Enter password or path to SSH key: ")
    key_type = input("Enter key type (pem, rsa, dsa, ed25519) or leave blank for password: ")

    ssh_manager.create_vm(name, ip_address, username, password_or_key_path, key_type)
    print(f"New Connection {name} created successfully.\n")

def manage_ssh_connections(ssh_manager):
    while True:
        print_section_header("Manage SSH Connections")
        print("[1]   List all connections")
        print("[2]   Edit a connection")
        print("[3]   Delete a connection")
        print("[4]   Back to main menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            list_connections(ssh_manager)
        elif choice == '2':
            edit_connection(ssh_manager)
        elif choice == '3':
            delete_connection(ssh_manager)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.\n")

def list_connections(ssh_manager):
    vms = ssh_manager.list_vms()
    if not vms:
        print("No connections found.")
        return

    print_section_header("Available Connections")
    print(f"{'No.':<5}|    {'Name':<20}  |   {'IP Address':<15}  |   {'Username':<10}")
    print("-" * 70)
    vm_names = list(vms.keys())
    for i, name in enumerate(vm_names, 1):
        vm = vms[name]
        print(f"{i:<3}  |   {name:<20}   |   {vm['ip_address']:<15}  |   {vm['username']:<10}")

def edit_connection(ssh_manager):
    vms = ssh_manager.list_vms()
    if not vms:
        print("No connections found.")
        return

    print_section_header("Edit Connection")
    print("[0] Back")
    vm_names = list(vms.keys())
    for i, name in enumerate(vm_names, 1):
        print(f"[{i}] {name}")

    try:
        choice = int(input("Enter the number of the connection to edit: "))
        if choice == 0:
            return
        if 1 <= choice <= len(vm_names):
            name = vm_names[choice - 1]
            vm = vms[name]
            print(f"Editing connection: {name}")

            ip_address = vm['ip_address']
            username = vm['username']
            password_or_key_path = vm['password_or_key_path']
            key_type = vm['key_type']

            if input(f"Current IP address is {ip_address}. Do you want to change it? (y/n): ").lower() == 'y':
                ip_address = input("Enter new IP address: ")

            if input(f"Current username is {username}. Do you want to change it? (y/n): ").lower() == 'y':
                username = input("Enter new username: ")

            if input(f"Current password or key path is {password_or_key_path}. Do you want to change it? (y/n): ").lower() == 'y':
                password_or_key_path = input("Enter new password or path to SSH key: ")

            if input(f"Current key type is {key_type}. Do you want to change it? (y/n): ").lower() == 'y':
                key_type = input("Enter new key type (pem, rsa, dsa, ed25519): ")

            ssh_manager.edit_vm(name, ip_address, username, password_or_key_path, key_type)
            print(f"\nConnection {name} updated successfully.\n")
        else:
            print("Invalid choice. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def delete_connection(ssh_manager):
    vms = ssh_manager.list_vms()
    if not vms:
        print("No connections found.")
        return

    print_section_header("Delete Connection")
    print("[0] Back")
    vm_names = list(vms.keys())
    for i, name in enumerate(vm_names, 1):
        print(f"[{i}] {name}")

    try:
        choice = int(input("Enter the number of the connection to delete: "))
        if choice == 0:
            return
        if 1 <= choice <= len(vm_names):
            name = vm_names[choice - 1]
            ssh_manager.delete_vm(name)
            print(f"\nConnection {name} deleted successfully.\n")
        else:
            print("Invalid choice. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def connect_to_vm(ssh_manager):
    vms = ssh_manager.list_vms()
    if not vms:
        print("No connections found.")
        return

    print_section_header("Available Connections")
    print("[0] Back")
    vm_names = list(vms.keys())
    for i, name in enumerate(vm_names, 1):
        print(f"[{i}] {name}")

    try:
        choice = int(input("Enter the number of the connection to use: "))
        if choice == 0:
            return
        if 1 <= choice <= len(vm_names):
            name = vm_names[choice - 1]
            vm = vms[name]
            print_section_header("Connect to VM")
            print(f"Connecting to {vm['ip_address']} as {vm['username']} in:")
            # Countdown timer
            for i in range(3, 0, -1):
                print(f"{i} seconds...")
                time.sleep(1)
            client = ssh_manager.connect_to_vm(
                vm['ip_address'],
                vm['username'],
                vm['password_or_key_path'],
                vm['key_type']
            )
            if client:
                print(f"Connected to {name} successfully.")
                # Start an interactive shell session
                channel = client.invoke_shell()
                print_section_header("Interactive SSH Session")
                print("Type your commands below.")
                try:
                    #inicializace shellu
                    command = ''
                    channel.send(command + '\n')
                    output = channel.recv(32000).decode('utf-8')
                    print(output, end='')
                    output = ''
                    while True:
                        #command = input(f"{vm['username']}@{name}:~$ ")
                        command = input()
                        if command.lower() in ["exit", "quit"]:
                            break
                        channel.send(command + "\n")
                        time.sleep(0.25)  # Small delay to ensure the command is processed
                        output = ""
                        while channel.recv_ready():
                            output += channel.recv(4096).decode('utf-8') #recieve ma doceela malo bytu
                        # Remove the echoed command from the output
                        #if output.startswith(command):
                        #    output = output[len(command):].strip()
                        print(output, end = '') 
                except KeyboardInterrupt:
                    print("Closing connection.")
                finally:
                    channel.close()
                    client.close()
                    print("Connection closed.")
            else:
                print(f"Failed to connect to {name}.")
        else:
            print("Invalid choice. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")