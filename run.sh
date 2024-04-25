#!/bin/bash

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
pip install -r requirements.txt telethon python-dotenv playwright-stealth

# Install Playwright and its dependencies
playwright install
playwright install-deps
# Run the Python script
python3 tarde.py
