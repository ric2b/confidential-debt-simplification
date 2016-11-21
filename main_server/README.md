0- `python3 manage.py makemigrations main_server_app` (if the models were changed)
1- `python3 manage.py sqlmigrate main_server_app 0001`
2- `python3 manage.py migrate`
3- `python3 manage.py runserver`