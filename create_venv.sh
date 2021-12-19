#!/bin/bash
echo "Updating package list"
sudo apt-get update

echo "Installing Python3-venv"
sudo apt-get install -y python3-venv

echo "Creating venv"
python -m venv venv
source venv.sh
./install.sh
pip3 install pyinstaller
pip3 install --upgrade pyinstaller
deactivate
