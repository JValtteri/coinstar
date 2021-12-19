#!/bin/bash

# Build
echo "Start Virtual Enviroment"
source venv/bin/activate
echo "Pyinstaller"
pip3 install pyinstaller
echo "Build Executible"
~/.local/bin/pyinstaller gui.py --onedir --noconsole -n coinstar_gui
echo "Exit Virtual Enviroment"
deactivate
