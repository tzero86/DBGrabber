# DBGrabber

DBGrabber is a script that fetches and decrypts DBeaver credentials from your user profile. It's ideal for when you don't remember that masked password.
![Sample Run](https://i.imgur.com/PQg223s.png)

## Features

- Detects the operating system and searches for the credentials file.
- Decrypts the credentials file using OpenSSL.
- Displays the decrypted database credentials in the terminal with colored output.

## Prerequisites

- Python 3.x
- OpenSSL installed and available in your system's PATH.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:

   ```bash
   python main.py
   ```

2. Follow the on-screen instructions to view your decrypted DBeaver credentials.


## Supported Operating Systems and Default Paths

The script supports the following operating systems and searches for the credentials file in these default paths:

- **Windows:**
  - `C:\Users\<username>\AppData\Roaming\DBeaverData\workspace6\General\.dbeaver\credentials-config.json`
  - `C:\Users\<username>\AppData\Local\Packages\DBeaverCorp.DBeaverCE_*\LocalCache\Roaming\DBeaverData\workspace6\General\.dbeaver\credentials-config.json` (Windows Store installation)

- **Linux:**
  - `/home/<username>/.local/share/DBeaverData/workspace6/General/.dbeaver/credentials-config.json`
  - `/home/<username>/snap/dbeaver-ce/320/.local/share/DBeaverData/workspace6/General/.dbeaver/credentials-config.json` (Snap installation)

- **macOS:**
  - `/Users/<username>/Library/DBeaverData/workspace6/General/.dbeaver/credentials-config.json`

This script is tested on Windows only. Linux and macOS support is experimental (testers welcome).

## License

This project is licensed under the MIT License.
