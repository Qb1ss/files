@echo off
chcp 65001 > nul

pip show telethon > nul
if errorlevel 1 (
    pip install telethon
)

pip show tgcrypto > nul
if errorlevel 1 (
    pip install tgcrypto
)

pip show pyrogram> nul
if errorlevel 1 (
    pip install pyrogram
)

:cmd
pause null