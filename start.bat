@ECHO OFF

start cmd.exe /C "cd . && workon rhe && code . && python manage.py runserver"

explorer "http://127.0.0.1:8000"