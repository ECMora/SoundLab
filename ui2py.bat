@echo off

SET PYTHON_PATH=C:\bin\EPD\Python27\
SET PYUIC_SUBPATH=Lib\site-packages\PyQt4\uic\
set UI_PATH=D:\dev\duetto\d-SoundLab\duetto-SoundLab\graphic_interface\UI_Files\
set PY_PATH=D:\dev\duetto\d-SoundLab\duetto-SoundLab\graphic_interface\windows\ui_python_files\

SET IN_FILE=%UI_PATH%%~nx1
SET OUT_FILE=%PY_PATH%%~n1.py
echo Input file: %IN_FILE%
echo Output file: %OUT_FILE%

%PYTHON_PATH%python.exe %PYTHON_PATH%%PYUIC_SUBPATH%pyuic.py "%IN_FILE%" -o "%OUT_FILE%"

pause

REM for %%f in (D:\dev\duetto\d-SoundLab\duetto-SoundLab\graphic_interface\UI_Files\*.ui) do (
	REM echo "Input file: %%~nxf"
	REM echo "Output file: %%~nf.py"
REM )

REM chdir "D:\setup\programming\python\rad\ui2py"
REM D:

REM @"C:\bin\EPD\Python27\python" "C:\bin\EPD\Python27\Lib\site-packages\PyQt4\uic\pyuic.py" %1 %2 %3 %4 %5 %6 %7 %8 %9
