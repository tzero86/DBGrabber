import os
import platform
import subprocess
import shutil
import json
import re
from pathlib import Path
import psutil
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)


def find_credentials_file(username):
    """Find the credentials-config.json file based on the OS."""
    system = platform.system()
    print(Fore.CYAN + f"[INFO] Detected Operating System: {system}")
    if system == "Windows":
        drives = [partition.device for partition in psutil.disk_partitions()]
        print(Fore.CYAN + f'[INFO] Drives detected: {drives}')
        for drive in drives:
            file_path = Path(
                drive) / f'Users/{username}/AppData/Roaming/DBeaverData/workspace6/General/.dbeaver/credentials-config.json'
            if file_path.exists():
                return file_path

            # Check for Windows Store installation path
            store_path = Path(
                drive) / f'Users/{username}/AppData/Local/Packages/DBeaverCorp.DBeaverCE_*/LocalCache/Roaming/DBeaverData/workspace6/General/.dbeaver/credentials-config.json'
            if store_path.exists():
                return file_path
    elif system == "Linux":
        file_path = Path.home() / '.local/share/DBeaverData/workspace6/General/.dbeaver/credentials-config.json'
        if file_path.exists():
            return file_path

        # Check for Snap installation path
        snap_path = Path.home() / f'snap/dbeaver-ce/320/.local/share/DBeaverData/workspace6/General/.dbeaver/credentials-config.json'
        if snap_path.exists():
            return snap_path
            return file_path
    elif system == "Darwin":  # macOS
        file_path = Path.home() / 'Library/DBeaverData/workspace6/General/.dbeaver/credentials-config.json'
        if file_path.exists():
            return file_path
    return None


def decrypt_file(encryption_key, initialization_vector, input_file, output_file):
    """Decrypt the file using OpenSSL."""
    # Check if OpenSSL is available
    if shutil.which("openssl") is None:
        print("[ERROR] OpenSSL is not installed or not found in PATH.")
        return 1, "OpenSSL not found"

    command = [
        'openssl', 'aes-128-cbc', '-d',
        '-K', encryption_key,
        '-iv', initialization_vector,
        '-in', str(input_file),
        '-out', str(output_file)
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.returncode, result.stderr


def main():
    print(Fore.MAGENTA + r"""

    ██████  ██████   ██████  ██████   █████  ██████  ██████  ███████ ██████  
    ██   ██ ██   ██ ██       ██   ██ ██   ██ ██   ██ ██   ██ ██      ██   ██ 
    ██   ██ ██████  ██   ███ ██████  ███████ ██████  ██████  █████   ██████  
    ██   ██ ██   ██ ██    ██ ██   ██ ██   ██ ██   ██ ██   ██ ██      ██   ██ 
    ██████  ██████   ██████  ██   ██ ██   ██ ██████  ██████  ███████ ██   ██ 
                                                                by @tzero86
        This Script fetches and decrypts DBeaver credentials from your user.
        Ideal for when you don't remember that masked password.                                                                                                                   
    """)
    print(Fore.RED + "DISCLAIMER: This script is tested on Windows only.\nLinux, and macOS support is "
                     "experimental (testers welcome). \n")

    encryption_key = "babb4a9f774ab853c96c2d653dfe544a"
    initialization_vector = "00000000000000000000000000000000"

    username = os.getlogin()
    print(Fore.CYAN + f"[INFO] Detected username: {username}")

    print(Fore.CYAN + f"[INFO] Searching for credentials file for user: {username}")
    file_path = find_credentials_file(username)
    if file_path:
        print(Fore.GREEN + f"[INFO] Credentials file found at: {file_path}")
    else:
        print(Fore.RED + "[ERROR] Credentials file not found.")

    if file_path:
        print(Fore.GREEN + f"[INFO] User profile found on drive: {file_path.drive}")
        print(Fore.CYAN + f"[INFO] Looking for file at: {file_path}")

        # Copy the file to the current directory
        destination = Path('./credentials-config.json')
        shutil.copy(file_path, destination)
        print(Fore.GREEN + "[SUCCESS] File copied successfully.")

        # Decrypt the file
        output_file = Path('./decrypted-output.txt')
        returncode, stderr = decrypt_file(encryption_key, initialization_vector, destination, output_file)

        if returncode == 0 and output_file.exists():
            print(Fore.GREEN + "[SUCCESS] Decryption completed successfully.")
            print(Style.BRIGHT + "------------------------------------------------------")
            print(Fore.YELLOW + "Decrypted Content below:👇")
            with output_file.open('r', encoding='latin-1') as file:
                content = file.read()
                # Extract JSON part using regex
                match = re.search(r'\{.*\}', content)
                if match:
                    json_content = match.group(0)
                    credentials = json.loads(json_content)
                    for db, details in credentials.items():
                        user = details['#connection']['user']
                        password = details['#connection']['password']
                        print(Fore.CYAN + f"\n|- Database: {db}")
                        print(Fore.CYAN + f"|--> User: {user}")
                        print(Fore.CYAN + f"|--> Password: {password}")
                else:
                    print(Fore.RED + "[ERROR] JSON content not found in the decrypted output.")
        else:
            print(Fore.RED + "[ERROR] Decryption failed.")
            print(stderr)
    else:
        print(Fore.RED + "[ERROR] User profile drive not found. Please check the configuration.")

    print(Fore.GREEN + "\n\n[BYE] Thanks for using DBGrabber! - by @tzero86 👽\n")


if __name__ == "__main__":
    main()
