#!/bin/bash
echo "Updating package list"
sudo apt-get update

echo "Installing pip3"
sudo apt-get -y install python3-pip

echo "Installing tkinter"
sudo apt-get install python3-tk -y

echo "Updating pip"
pip3 install --upgrade pip

echo "Installing requirements"
pip3 install -r requirements.txt
