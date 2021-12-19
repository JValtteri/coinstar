#!/bin/bash
echo "Installing pip3"
sudo apt-get -y install python3-pip

echo "Updating pip"
pip3 install --upgrade pip

echo "Installing requirements"
pip3 install -r requirements.txt

echo "Installing tkinter"
sudo apt-get install python3-tk -y
