#!/bin/bash

# Build
echo "Start Virtual Enviroment"
source venv/bin/activate
echo "Build Executible"
pyinstaller gui.py --onedir --noconsole -n coinstar_gui
echo "Exit Virtual Enviroment"
deactivate
