#Steps to install this

## 1. First take git clone of this repository.
## 2. Make Virtualenv and activate that.
## 3. install requirements.txt.
## 4. Run makemigration and migrate command.
## 5. Creat Superuser and login to admin portal with '/manage-admin/' url.
## 6. Fill data manually in 'Index' table one by one:niftynext,nifty50,niftybank,niftymidcap,niftyfinanace.
## 7. Run th following command :
###  a. python manage.py uplaod_data NF50.csv
###  b. python manage.py uplaod_data NIFTYBANK.csv
###  c. python manage.py uplaod_data NIFTYFINANCE.csv
###  d. python manage.py uplaod_data NIFTYMIDCAP.csv
###  e. python manage.py uplaod_data NIFTYNEXT.csv

## DATABASE IS SET NOW.
## 8. test the api on: 'api/v1/get-data/<int:index_id>/start_date=2025-01-01&end_date=2025-02-10&filters=OPEN>23000' or 'api/v1/get-data/<int:index_id>/start_date=2025-01-01&end_date=2025-02-10'
