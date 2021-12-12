#!/bin/bash
python -m venv venv
source venv.sh
./install.sh
pip3 install pyinstaller
pip3 install --upgrade pyinstaller
deactivate
