@echo off
chcp 65001 >nul
title Minecraft Launcher
cd /d "%~dp0"

:: Настройки
set "GITHUB_REPO=lixynhay/mc-terminal-launcher"
set "GITHUB_API=https://api.github.com/repos/%GITHUB_REPO%/releases/latest"
set "SCRIPT_NAME=launcher.py"
set "VERSION_FILE=version.txt"
set "LANG_FILE=language.json"

:: Включаем отложенное расширение переменных
setlocal enabledelayedexpansion

:: Выбор языка
:select_language
cls
echo ====================================================
echo         MINECRAFT LAUNCHER
echo ====================================================
echo.
echo Select language / Выберите язык:
echo.
echo [1] English
echo [2] Русский
echo.

set /p lang_choice="Choice [1-2]: "

if "%lang_choice%"=="1" set "LANG=en" & goto :set_language
if "%lang_choice%"=="2" set "LANG=ru" & goto :set_language
goto :select_language

:set_language
:: Сохраняем язык в файл
echo {"language": "%LANG%"} > "%LANG_FILE%"

if "%LANG%"=="en" goto :en_menu
if "%LANG%"=="ru" goto :ru_menu

:en_menu
cls
echo ====================================================
echo         MINECRAFT LAUNCHER UPDATER
echo ====================================================
echo.

:: Show current version
if exist "%VERSION_FILE%" (
    set /p CURRENT_VERSION=<"%VERSION_FILE%"
    echo [📌] Current version: %CURRENT_VERSION%
) else (
    echo [📌] Version not detected
)
echo.

echo [1] Check for updates
echo [2] Launch Minecraft
echo [3] Install libraries
echo [4] Clean cache
echo [5] Change language
echo [0] Exit
echo.

set /p choice="Choose [0-5]: "

if "%choice%"=="1" goto :check_updates_en
if "%choice%"=="2" goto :launch_launcher
if "%choice%"=="3" goto :install_libs
if "%choice%"=="4" goto :clean_cache
if "%choice%"=="5" goto :select_language
if "%choice%"=="0" goto :exit
goto :en_menu

:ru_menu
cls
echo ====================================================
echo         MINECRAFT LAUNCHER UPDATER
echo ====================================================
echo.

:: Show current version
if exist "%VERSION_FILE%" (
    set /p CURRENT_VERSION=<"%VERSION_FILE%"
    echo [📌] Текущая версия: %CURRENT_VERSION%
) else (
    echo [📌] Версия не определена
)
echo.

echo [1] Проверить обновления
echo [2] Запустить Minecraft
echo [3] Установить библиотеки
echo [4] Очистить кэш
echo [5] Сменить язык
echo [0] Выход
echo.

set /p choice="Выберите [0-5]: "

if "%choice%"=="1" goto :check_updates_ru
if "%choice%"=="2" goto :launch_launcher
if "%choice%"=="3" goto :install_libs
if "%choice%"=="4" goto :clean_cache
if "%choice%"=="5" goto :select_language
if "%choice%"=="0" goto :exit
goto :ru_menu

:check_updates_en
cls
echo ====================================================
echo         CHECKING FOR UPDATES
echo ====================================================
echo.

echo [1/4] Checking GitHub...
echo.

:: Проверяем подключение к интернету
ping -n 2 github.com >nul 2>&1
if errorlevel 1 (
    echo [❌] No internet connection!
    echo.
    echo Please check your internet connection and try again.
    echo.
    pause
    goto :en_menu
)

:: Получаем информацию о последнем релизе
powershell -Command "& {
    try {
        $response = Invoke-RestMethod -Uri '%GITHUB_API%' -Headers @{'User-Agent'='Mozilla/5.0'} -ErrorAction Stop
        $latest = $response.tag_name -replace '^v', ''
        $downloadUrl = ($response.assets | Where-Object { $_.name -eq '%SCRIPT_NAME%' }).browser_download_url
        $changelog = $response.body
        
        Write-Host 'LATEST_VERSION='$latest
        Write-Host 'DOWNLOAD_URL='$downloadUrl
        Write-Host 'CHANGELOG='$changelog
    } catch {
        Write-Host 'ERROR='$_.Exception.Message
    }
}" > "%temp%\github_info.tmp"

:: Парсим результаты
set "LATEST_VERSION="
set "DOWNLOAD_URL="
set "CHANGELOG="
set "ERROR_MSG="

for /f "usebackq delims=" %%a in ("%temp%\github_info.tmp") do (
    set "line=%%a"
    if "!line:~0,14!"=="LATEST_VERSION=" set "LATEST_VERSION=!line:~14!"
    if "!line:~0,12!"=="DOWNLOAD_URL=" set "DOWNLOAD_URL=!line:~12!"
    if "!line:~0,8!"=="CHANGELOG=" set "CHANGELOG=!line:~8!"
    if "!line:~0,6!"=="ERROR=" set "ERROR_MSG=!line:~6!"
)

del "%temp%\github_info.tmp"

:: Проверяем ошибки
if defined ERROR_MSG (
    echo [❌] Error checking updates:
    echo    !ERROR_MSG!
    echo.
    echo Possible reasons:
    echo   • GitHub API limit reached
    echo   • Repository not found
    echo   • No internet connection
    echo.
    pause
    goto :en_menu
)

if not defined LATEST_VERSION (
    echo [❌] Could not get version info
    echo.
    echo Make sure the repository exists and has releases.
    echo.
    pause
    goto :en_menu
)

:: Получаем текущую версию
if exist "%VERSION_FILE%" (
    set /p CURRENT_VERSION=<"%VERSION_FILE%"
) else (
    set "CURRENT_VERSION=0.0.0"
)

echo [✅] Current version: %CURRENT_VERSION%
echo [✅] Latest version: %LATEST_VERSION%
echo.

:: Сравниваем версии
if "%CURRENT_VERSION%"=="%LATEST_VERSION%" (
    echo ====================================================
    echo         YOU HAVE THE LATEST VERSION!
    echo ====================================================
    echo.
    pause
    goto :en_menu
) else (
    echo ====================================================
    echo         UPDATE AVAILABLE!
    echo ====================================================
    echo.
    
    if defined CHANGELOG (
        echo What's new:
        echo ------------------------
        echo !CHANGELOG!
        echo ------------------------
        echo.
    )
    
    echo [1] Update now
    echo [2] Skip
    echo.
    set /p up_choice="Choose [1-2]: "
    
    if "!up_choice!"=="1" goto :download_update
    goto :en_menu
)

:check_updates_ru
cls
echo ====================================================
echo         ПРОВЕРКА ОБНОВЛЕНИЙ
echo ====================================================
echo.

echo [1/4] Проверка GitHub...
echo.

:: Проверяем подключение к интернету
ping -n 2 github.com >nul 2>&1
if errorlevel 1 (
    echo [❌] Нет подключения к интернету!
    echo.
    echo Проверьте интернет-соединение и попробуйте снова.
    echo.
    pause
    goto :ru_menu
)

:: Получаем информацию о последнем релизе
powershell -Command "& {
    try {
        $response = Invoke-RestMethod -Uri '%GITHUB_API%' -Headers @{'User-Agent'='Mozilla/5.0'} -ErrorAction Stop
        $latest = $response.tag_name -replace '^v', ''
        $downloadUrl = ($response.assets | Where-Object { $_.name -eq '%SCRIPT_NAME%' }).browser_download_url
        $changelog = $response.body
        
        Write-Host 'LATEST_VERSION='$latest
        Write-Host 'DOWNLOAD_URL='$downloadUrl
        Write-Host 'CHANGELOG='$changelog
    } catch {
        Write-Host 'ERROR='$_.Exception.Message
    }
}" > "%temp%\github_info.tmp"

:: Парсим результаты
set "LATEST_VERSION="
set "DOWNLOAD_URL="
set "CHANGELOG="
set "ERROR_MSG="

for /f "usebackq delims=" %%a in ("%temp%\github_info.tmp") do (
    set "line=%%a"
    if "!line:~0,14!"=="LATEST_VERSION=" set "LATEST_VERSION=!line:~14!"
    if "!line:~0,12!"=="DOWNLOAD_URL=" set "DOWNLOAD_URL=!line:~12!"
    if "!line:~0,8!"=="CHANGELOG=" set "CHANGELOG=!line:~8!"
    if "!line:~0,6!"=="ERROR=" set "ERROR_MSG=!line:~6!"
)

del "%temp%\github_info.tmp"

:: Проверяем ошибки
if defined ERROR_MSG (
    echo [❌] Ошибка проверки обновлений:
    echo    !ERROR_MSG!
    echo.
    echo Возможные причины:
    echo   • Достигнут лимит GitHub API
    echo   • Репозиторий не найден
    echo   • Нет интернета
    echo.
    pause
    goto :ru_menu
)

if not defined LATEST_VERSION (
    echo [❌] Не удалось получить информацию о версии
    echo.
    echo Убедитесь, что репозиторий существует и имеет релизы.
    echo.
    pause
    goto :ru_menu
)

:: Получаем текущую версию
if exist "%VERSION_FILE%" (
    set /p CURRENT_VERSION=<"%VERSION_FILE%"
) else (
    set "CURRENT_VERSION=0.0.0"
)

echo [✅] Текущая версия: %CURRENT_VERSION%
echo [✅] Последняя версия: %LATEST_VERSION%
echo.

:: Сравниваем версии
if "%CURRENT_VERSION%"=="%LATEST_VERSION%" (
    echo ====================================================
    echo         У ВАС АКТУАЛЬНАЯ ВЕРСИЯ!
    echo ====================================================
    echo.
    pause
    goto :ru_menu
) else (
    echo ====================================================
    echo         ДОСТУПНО ОБНОВЛЕНИЕ!
    echo ====================================================
    echo.
    
    if defined CHANGELOG (
        echo Что нового:
        echo ------------------------
        echo !CHANGELOG!
        echo ------------------------
        echo.
    )
    
    echo [1] Обновить сейчас
    echo [2] Пропустить
    echo.
    set /p up_choice="Выберите [1-2]: "
    
    if "!up_choice!"=="1" goto :download_update
    goto :ru_menu
)

:download_update
cls
echo ====================================================
echo         DOWNLOADING UPDATE / СКАЧИВАНИЕ ОБНОВЛЕНИЯ
echo ====================================================
echo.

if not defined DOWNLOAD_URL (
    echo [❌] Download link not found
    echo.
    pause
    if "%LANG%"=="en" goto :en_menu
    goto :ru_menu
)

:: Create backup
echo [1/4] Creating backup...
if exist "%SCRIPT_NAME%" (
    copy "%SCRIPT_NAME%" "%SCRIPT_NAME%.backup_%CURRENT_VERSION%" >nul
    echo   ✅ Backup created: %SCRIPT_NAME%.backup_%CURRENT_VERSION%
)

:: Download new version
echo [2/4] Downloading new version...
echo.

powershell -Command "& {
    try {
        Write-Host '   Downloading...'
        Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%SCRIPT_NAME%.new' -ErrorAction Stop
        Write-Host '   ✅ Download complete'
    } catch {
        Write-Host '   ❌ Download error: ' $_.Exception.Message
        exit 1
    }
}"

if errorlevel 1 (
    echo.
    echo [❌] Download error
    echo.
    pause
    if "%LANG%"=="en" goto :en_menu
    goto :ru_menu
)

:: Replace old file
echo [3/4] Installing update...
move /y "%SCRIPT_NAME%.new" "%SCRIPT_NAME%" >nul

:: Update version file
echo %LATEST_VERSION% > "%VERSION_FILE%"

echo [4/4] Update complete!
echo.
echo ====================================================
echo         UPDATE SUCCESSFUL / ОБНОВЛЕНИЕ УСПЕШНО
echo ====================================================
echo.
echo New version: %LATEST_VERSION%
echo.
pause
if "%LANG%"=="en" goto :en_menu
goto :ru_menu

:launch_launcher
cls
echo ====================================================
echo         LAUNCHING MINECRAFT / ЗАПУСК MINECRAFT
echo ====================================================
echo.

:: Check if launcher exists
if not exist "%SCRIPT_NAME%" (
    echo [❌] File %SCRIPT_NAME% not found!
    echo.
    pause
    if "%LANG%"=="en" goto :en_menu
    goto :ru_menu
)

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [❌] Python not found!
    echo.
    echo Download Python from: https://www.python.org/downloads/
    echo.
    pause
    if "%LANG%"=="en" goto :en_menu
    goto :ru_menu
)

:: Check library
python -c "import minecraft_launcher_lib" >nul 2>&1
if errorlevel 1 (
    echo [📦] Installing minecraft-launcher-lib...
    pip install minecraft-launcher-lib -q
)

python -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo [📦] Installing psutil...
    pip install psutil -q
)

echo [🚀] Launching...
echo.
python "%SCRIPT_NAME%"

echo.
pause
if "%LANG%"=="en" goto :en_menu
goto :ru_menu

:install_libs
cls
echo ====================================================
echo         INSTALLING LIBRARIES / УСТАНОВКА БИБЛИОТЕК
echo ====================================================
echo.

echo [1/3] Updating pip...
python -m pip install --upgrade pip -q
if errorlevel 1 (
    echo [⚠️] Failed to update pip, continuing anyway...
) else (
    echo   ✅ Done
)

echo.
echo [2/3] Installing minecraft-launcher-lib...
pip install minecraft-launcher-lib -q
if errorlevel 1 (
    echo [❌] Failed to install minecraft-launcher-lib
    echo.
    pause
    if "%LANG%"=="en" goto :en_menu
    goto :ru_menu
) else (
    echo   ✅ Done
)

echo.
echo [3/3] Installing psutil...
pip install psutil -q
if errorlevel 1 (
    echo [❌] Failed to install psutil
    echo.
    pause
    if "%LANG%"=="en" goto :en_menu
    goto :ru_menu
) else (
    echo   ✅ Done
)

echo.
echo ====================================================
echo         INSTALLATION COMPLETE / УСТАНОВКА ЗАВЕРШЕНА
echo ====================================================
echo.
pause
if "%LANG%"=="en" goto :en_menu
goto :ru_menu

:clean_cache
cls
echo ====================================================
echo         CLEANING CACHE / ОЧИСТКА КЭША
echo ====================================================
echo.

:: Remove backups
echo [1/4] Removing backups...
del /q "*.backup_*" 2>nul
echo   ✅ Done

:: Remove __pycache__
echo [2/4] Removing __pycache__...
if exist "__pycache__" (
    rmdir /s /q "__pycache__"
    echo   ✅ Removed
) else (
    echo   ⏭️ Not found
)

:: Remove logs
echo [3/4] Removing logs...
if exist "logs" (
    del /q "logs\*.log" 2>nul
    echo   ✅ Removed
) else (
    echo   ⏭️ Not found
)

:: Clean temp files
echo [4/4] Cleaning temp files...
del /q "%temp%\github_info.tmp" 2>nul
echo   ✅ Done

echo.
echo ====================================================
echo         CLEANUP COMPLETE / ОЧИСТКА ЗАВЕРШЕНА
echo ====================================================
echo.
pause
if "%LANG%"=="en" goto :en_menu
goto :ru_menu

:exit
echo.
echo 👋 Goodbye / До свидания
timeout /t 2 /nobreak >nul
exit /b