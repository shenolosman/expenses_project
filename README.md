# Django expenses

- docker run --name your_postgres_container_name -e POSTGRES_PASSWORD=mypassword -p 5430:5432 -d postgres
- docker exec -it your_postgres_container_name createdb -U postgres [dbname] or docker exec -it mypostgress4django psql -U postgres
- \dt => tables

pipenv shell => to get in virtual env