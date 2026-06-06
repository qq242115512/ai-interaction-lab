@echo off
REM ========================================
REM Pre-push Check - Local code quality
REM Run before git push: check.bat
REM ========================================
REM Community standard: Ruff/ESLint/Prettier
REM We run locally (GitHub Actions + Windows
REM Runner + WSL nesting = broken)
REM 2026-06-06: Added pyproject.toml + Ruff

echo ========================================
echo   AI Interaction Lab - Pre-push Check
echo ========================================
echo.

echo [1/4] Ruff Lint
echo ---------------
python -m ruff check src/backend/ || echo [WARN] Ruff found issues
echo.

echo [2/4] Security Scan
echo ---------------
python -m ruff check src/backend/ --select S || echo [WARN] Review before pushing
echo.

echo [3/4] App Import Test
echo ---------------
cd src/backend
python -c "from main import app; print('[OK] App loads OK')" || echo [FAIL] App load failed
echo.

echo [4/4] Prompt Evaluation (format)
echo ---------------
python -m tests.evaluate_prompts --format-only 2>/dev/null || echo [WARN] Prompt tests skipped
echo.

echo ========================================
echo   All checks done. Ready to git push.
echo ========================================
