@echo off
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
pyinstaller --onefile --windowed --name "EnglishDictionary" "python dictionary(phase 2).py"
if exist dist\EnglishDictionary.exe (
    echo.
    echo Build complete: dist\EnglishDictionary.exe
) else (
    echo.
    echo Build failed. Check the PyInstaller output above.
)
pause
