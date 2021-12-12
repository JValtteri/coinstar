:: build game
@echo Start Virtual Enviroment
cd venv\Scripts
call activate.bat
cd ../..
@echo Build EXE
pyinstaller gui.py --onedir --noconsole -n coinstar_gui
@echo Exit Virtual Enviroment
deactivate
pause
