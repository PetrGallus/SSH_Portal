import yaml
from utils.ssh_manager import SSHManager
from menu.menu import display_menu

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    config = load_config('src/config/config.yaml')
    ssh_manager = SSHManager(config)
    
    while True:
        if not display_menu(ssh_manager):
            break

if __name__ == "__main__":
    main()