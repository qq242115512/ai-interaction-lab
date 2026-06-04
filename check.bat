@echo off
REM =================================================
REM push 之前跑这个——代码规范 + 安全检查 + 测试
REM 跑完没错误再 push。任何一步报错，先修再 push
REM =================================================

echo ===================================================
echo 1/3 代码规范检查（Ruff）
echo ===================================================
pip install ruff -q 2>nul
ruff check src/backend/ --output-format concise
if %errorlevel% neq 0 (
    echo ^^⚠️ Ruff 检查有提醒——请修复后重新 push
) else (
    echo ✅ 代码规范检查通过
)

echo.
echo ===================================================
echo 2/3 安全检查（API Key / 私钥泄露）
echo ===================================================
findstr /s /i /c:"sk-" src\backend\*.py 2>nul | findstr /v /c:".env" | findstr /v /c:"__pycache__" >nul
if %errorlevel% equ 0 (echo ❌ 发现疑似 API Key 硬编码) else (echo ✅ 无 API Key 泄露)

findstr /s /c:"PRIVATE KEY" src\*.py src\*.html 2>nul >nul
if %errorlevel% equ 0 (echo ❌ 发现私钥泄露) else (echo ✅ 无私钥泄露)

findstr /s /c:"@Fsy2006" src\*.py src\*.html 2>nul >nul
if %errorlevel% equ 0 (echo ❌ 发现密码硬编码) else (echo ✅ 无密码硬编码)

echo.
echo ===================================================
echo 3/3 自动化测试（pytest）
echo ===================================================
pip install pytest httpx -q 2>nul
cd src\backend
python -m pytest . -v --tb=short 2>nul
if %errorlevel% equ 0 (
    echo ✅ 所有测试通过
) else (
    echo ⚠️ 有测试未通过——请修复后重新 push
)
cd ..\..

echo.
echo ===================================================
echo 检查完成——如果上面没有错误，可以放心 git push
echo ===================================================
pause
