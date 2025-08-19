@echo off
echo Generating BROski project structure...
tree "%~dp0" /F /A > "%~dp0BROski_Tree.txt"
echo Structure saved to BROski_Tree.txt
pause
