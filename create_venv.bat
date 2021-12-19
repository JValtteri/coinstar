@echo "Creating venv"
python -m venv venv
call venv.sh
./install.sh
pip3 install pyinstaller
pip3 install --upgrade pyinstaller
deactivate
