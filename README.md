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


## Disclaimer

This script is tested on Windows only. Linux and macOS support is experimental (testers welcome).

## License

This project is licensed under the MIT License.
