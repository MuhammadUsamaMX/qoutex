#!/bin/bash
#https://ubuntuhandbook.org/index.php/2022/10/python-3-11-released-how-install-ubuntu/
# Here's how you can install pip for Python 3.11:

# Download the get-pip.py script:
# bash
# Copy code
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# Install pip for Python 3.11 using the downloaded script:
# bash
# Copy code
# python3.11 get-pip.py
# Verify that pip is installed for Python 3.11:
# bash
# Copy code
# python3.11 -m pip --version
# This should install pip for Python 3.11 and allow you to use it to install Python packages. Let me know if you encounter any issues!
#sudo apt update
# sudo apt install python3-dev build-essential libssl-dev








# Set timezone
export TZ=Asia/Karachi
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install necessary packages
apt-get update
apt-get install -y software-properties-common python3.11 python3-pip git

# Clone the repository
git clone -b AutoTrade https://github.com/MuhammadUsamaMX/qoutex.git ~/qoutex

# Set the working directory
cd ~/qoutex

# Install Python dependencies
pip install -r requirements.txt 
pip install telethon python-dotenv playwright-stealth schedule pyfiglet

# Install Playwright and its dependencies
playwright install && playwright install-deps
# Run the Python script
python3 run.py
