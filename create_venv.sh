#!/bin/bash
python -m venv venv
./venv.sh
./install.sh
pip install pyinstaller
pip install --upgrade pyinstaller
deactivate
