# Django expenses

- docker run --name your_postgres_container_name -e POSTGRES_PASSWORD=mypassword -p 5430:5432 -d postgres
- docker exec -it your_postgres_container_name createdb -U postgres [dbname] or docker exec -it mypostgress4django psql -U postgres
- \dt => tables

- to run code cd 
- pipenv shell => to get in virtual env
- expenseswebsite, py manage.py runserver

- python manage.py createsuperuser => to create admin users
- py.exe .\manage.py merge => to merge things
-----------------

- under main folder => py manage.py shell
- from django.contrib.auth.models import User
- users=User.objects.all()
- users=User.objects.get(username='admin')
- users.email
- users.password => auto hashed
- users.is_active => bool
- quit()
--------------------