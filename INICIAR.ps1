$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Join-Path $PSScriptRoot 'backend')
& (Join-Path $PSScriptRoot '.venv/Scripts/python.exe') manage.py runserver 127.0.0.1:8016
