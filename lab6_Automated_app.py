"""

# Lab 6 - Automated App Installation

# Purpose : The following Script installs VLC Media Player silently into the machine if
            run in Administrator Mode

"""

# Script Starts here

import hashlib
import requests
import os
import subprocess


def main():
    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):
        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)


def get_expected_sha256():
    # Send GET message to download the file
    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe.sha256'
    resp_msg = requests.get(file_url)
    # Check
    # whether the download was successful
    if resp_msg.status_code == requests.codes.ok:
        # Extract text file content from
        # response message
        file_content = resp_msg.text
        value = file_content.split('*')
        return value[0].replace(" ", "")


def download_installer():
    # Send GET message to download the file
    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe'
    resp_msg = requests.get(file_url)
    # Check
    # whether the download was successful
    if resp_msg.status_code == requests.codes.ok:
        # Extract text file content from
        # response message
        file_content = resp_msg.content
        return file_content


def installer_ok(installer_data, expected_sha256):
    # Calculate SHA-256 hash value
    image_hash = hashlib.sha256(installer_data).hexdigest()

    # Checking the Hash value
    if image_hash == expected_sha256:
        print('Hash value matches')
        return True


def save_installer(installer_data):
    # Save the file to disk
    location = r'C:\vlcSetup.exe'
    with open(location, 'wb') as file:
        file.write(installer_data)

    return location


def run_installer(installer_path):
    # installer runs here
    subprocess.run([installer_path, '/L=1033', '/S'])


def delete_installer(installer_path):
    # Removing the installer file
    os.remove(installer_path)


if __name__ == '__main__':
    main()
