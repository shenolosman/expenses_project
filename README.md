# Django expenses

- docker run --name your_postgres_container_name -e POSTGRES_PASSWORD=mypassword -p 5430:5432 -d postgres
- docker exec -it your_postgres_container_name createdb -U postgres [dbname] or docker exec -it mypostgress4django psql -U postgres
- \dt => db list
- \c __database__ => connect to a database
- \d __table__ => show table definition

- to run code cd 
- pipenv shell => to get in virtual env
- expenseswebsite, py manage.py runserver

- py .\manage.py startapp userprefences => to create new module
- py manage.py makemigrations => create migration file for sql
- py manage.py migrate => migrates to sql server
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

### https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/
- manage.py check --deploy


-------------------------   
- import pdb 
- pdb.set_trace() => helps to debugs in console ["can be written any of variable in that file that trace defined"]