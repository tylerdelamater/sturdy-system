set FLASK_APP=./src/main.py
set FLASK_ENV=development
virtualenv virtualenvpath
powershell -ExecutionPolicy ByPass -File "c:\Users\tdelamater2\projects\EventFinder\sturdy-system\virtualenvpath\Scripts\activate.ps1"
flask run -h 0.0.0.0