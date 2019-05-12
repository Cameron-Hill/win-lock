@echo off
echo Working directory : %cd%
echo Script Location : %~dp0
echo attempting to activate environemnt:
REM source activate win-lock (should explicitly set python path)
echo writing text file:
python %~dp0write_a_file.pyw