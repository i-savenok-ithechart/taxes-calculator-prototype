# taxes-calculater-prototype

## how to run locally:
### 1. With Docker-compose:
Create pg volume with:
>sudo docker volume create --name=taxes_calculator_prot_pg_data

Build and run:
>sudo docker-compose up

App should be running on <b>localhost:8000</b>. Check the status with:
>curl --location --request GET 'http://localhost:8008/health/'

>curl --location --request PUT 'http://localhost:8008/api/v1/taxes/?detailed=true&year=2022' \
--header 'Content-Type: application/json' \
--data-raw '{
    "annual_salary_amount": "500"
}'
