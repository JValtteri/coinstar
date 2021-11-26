#!/bin/bash
echo "Updating pip"
pip3 install --upgrade pip

echo "Installing requirements"
pip3 install -r requirements.txt
