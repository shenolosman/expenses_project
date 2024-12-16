# Django expenses

- docker run --name mypostgress4django -e POSTGRES_PASSWORD=mypassword -p 5430:5432 -d postgres
- docker exec -it mypostgress4django psql -U myuser
- \dt => tables