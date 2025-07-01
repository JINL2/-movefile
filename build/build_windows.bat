@echo off
echo ====================================
echo Workflow Automation Build Script
echo ====================================
echo.

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python이 설치되지 않았습니다!
    echo Python을 먼저 설치해주세요: https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] 필요한 패키지 설치 중...
pip install pyinstaller requests flask flask-cors

echo.
echo [2/4] Step 1 - Supabase Polling Service 빌드 중...
pyinstaller --onefile --name "Step1_Supabase_Polling" --icon=NONE step1_polling_service.py

echo.
echo [3/4] Step 2 - API Server 빌드 중...
pyinstaller --onefile --name "Step2_API_Server" --hidden-import=flask --hidden-import=flask_cors --icon=NONE step2_api_server.py

echo.
echo [4/4] 빌드 정리 중...
REM spec 파일과 빌드 폴더 정리
rmdir /s /q build
del *.spec

echo.
echo ====================================
echo 빌드 완료!
echo ====================================
echo.
echo 실행 파일 위치:
echo - dist\Step1_Supabase_Polling.exe
echo - dist\Step2_API_Server.exe
echo.
echo 실행 방법:
echo 1. Step2_API_Server.exe를 먼저 실행
echo 2. Step1_Supabase_Polling.exe 실행
echo.
pause
