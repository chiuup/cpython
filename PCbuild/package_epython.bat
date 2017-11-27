@echo off

goto Run
:Run
setlocal
set platf=Win32
set conf=Release
set dir=%~dp0
set output=%dir%

:CheckOpts
if "%~1"=="-c" (set conf=%2) & shift & shift & goto CheckOpts
if "%~1"=="-p" (set platf=%2) & shift & shift & goto CheckOpts

if "%platf%"=="Win32" (set output=%dir%Win32\) & goto SetConf
if "%platf%"=="x64" (
    if exist "%dir%\amd64" (set output=%dir%amd64\) & goto SetConf
    if exist "%dir%\x86_amd64" (set output=%dir%x86_amd64\) & goto SetConf
)
goto Error

:SetConf
if "%conf%"=="Release" (set python=%output%python.exe) & goto FindPython
if "%conf%"=="Debug" (set python=%output%python_d.exe) & goto FindPython
goto Error

:FindPython
if not exist %python% (goto Error)

%python% -m compileall -b -qq %dir%..\Lib\ 
%python% -S -s -E %dir%compile_pyc.py -c %conf% -p %platf%
%python% -S -s -E %dir%package_epython.py -p %platf% -c %conf%

exit /b 127

:Error
echo Cannot find python.exe