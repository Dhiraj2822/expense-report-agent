@echo off
title Expense Report Agent — Final Jury Demo Launcher
color 0B
echo =====================================================================
echo    EXPENSE REPORT AGENT - FINAL JURY DEMO LAUNCHER (GROUP 4)
echo =====================================================================
echo.
echo Launching Streamlit Interactive Observability Dashboard...
echo Local URL: http://localhost:8501
echo.
cd /d "%~dp0..\.."
streamlit run streamlit_app.py
pause
