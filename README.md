- Create directory for project and then clone it:
```
mkdir contacts_db && cd contacts_db
git clone https://github.com/mikhail1706/contacts_db.git
```

- In base directory create directory for logs and local.py file 
```
mkdir logs
cp config/_local.py config/local.py
```

- Create venv
```
python3 -m  venv venv
```

- Install libs and apply migrations

````
source venv/bin/activate/
pip install --upgrade pip
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python manage.py runserver
````
open [localhost](http://127.0.0.1:8000)