@echo off
goto Run

:Run
setlocal
set dir=%~dp0
set forced=false


:CheckOpts
if "%~1"=="-f" (set forced=true) & shift & goto CheckOpts

if %forced% equ true (
    echo WHAT TRUE
    call %dir%build_elib.bat -e -p x64 -r
    call %dir%build_elib.bat -e -p x64 -d -r
    call %dir%build_elib.bat -e -p Win32 -r
    call %dir%build_elib.bat -e -p Win32 -d -r
)
if %forced% equ false (
    echo WHAT FALSE
    call %dir%build_elib.bat -e -p x64
    call %dir%build_elib.bat -e -p x64 -d
    call %dir%build_elib.bat -e -p Win32
    call %dir%build_elib.bat -e -p Win32 -d
)
python build_full.py