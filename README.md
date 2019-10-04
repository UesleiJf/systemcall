# README Olist

## Description

This application was developed using the Python language and Django for web framework.

For the development of the Rest API, the use of the DRF.

### Work environment details

* OS:	Ubuntu 16.04 LTS
* IDE: PyCharm Community
* Terminal: Terminal
* Database: sqlite3

### Library Versions

* Python:	3.6
* Django:	2.2
* Babel: 2.6.0
* Django Rest Framework: 3.9.3
* dj-database-url: 0.5.0
* dj-static: 0.0.6
* python-dateutil: 2.8.0
* django-rest-swagger: 2.2.0

### Installation

First, you need to clone this project from Bitbucket:

    git clone git@bitbucket.org:uesleijfs/systemcallolist.git

This project run under Python 3.6 and Django 2.2

After clone, you need to install all the requirements. 

The Python >= 3.3 comes with venv to creating lightweight "virtual environments".

For this project, python3.6 was used

For full documentation for venv, you can see here:
https://docs.python.org/3/library/venv.html

To create an enviroment, run:

    python3.6 -m venv venv
    
    . venv/bin/activate

Run the command below to update the pip and avoid dependency conflicts when installing requirements.txt

    pip install --upgrade pip

Navigate to the directory /systemcall/ and execute the commands below

Now, you can install al the project requirements:

    pip install -r requirements.txt

After this, just execute the commands makemigrations and migrate to create project tables

    python3.6 manage.py makemigrations

    python3.6 manage.py migrate

    python3.6 manage.py collectstatic

Now, you can start the project:

    python3.6 manage.py runserver

### Tests

To run test over this project, just execute the command below in console:

    python3.6 manage.py test

## API

This project has two end points: registercall and phonebill

http://localhost:8000/registercall/

http://localhost:8000/phonebill/

### registercall - for creating phone calls. 

Differentiated by call_type: Start(1) or End(2)

Examples for searching and create register call:

METHOD POST

> /registercall/

```json
{
    "type_call": 1, 
    "timestamp_call": "2019-04-10 15:10:12",
    "id_call": 70,
    "source_call": "99988526423",
    "destination_call": "62999907744"
}
```

```json
{
    "type_call": 2,
    "timestamp_call": "2019-04-10 15:59:33",
    "id_call": 70,
    "source_call": null,
    "destination_call": null
}
```

METHOD GET 

> /registercall/

```json
[
    {
        "id": 1,
        "type_call": 1,
        "timestamp_call": "2019-04-10T15:10:12Z",
        "id_call": 70,
        "source_call": "99988526423",
        "destination_call": "62999907744"
    },
    {
        "id": 2,
        "type_call": 2,
        "timestamp_call": "2019-04-10T15:59:33Z",
        "id_call": 70,
        "source_call": null,
        "destination_call": null
    }
]

```

### phone bill - for creating phone bills

Examples for searching and create Phone Bill:
Searches for all number calls made in the reported period or
if the period field is not informed (can be NULL)
the phone bill searches the last month you have closed.
 

METHOD POST

```json
{
   "period": "04/2019",
   "source_call": "99988526423",
   "bill": []
}

```

METHOD GET 

> /phonebill/

```json
{
    "id": 1,
    "period": "04/2019",
    "source_call": "99988526423",
    "bill": [
        "id: 1 | phone_bill: Source Call: 99988526423 | Period: 04/2019 | destination_call: 62999907744 | duration_call: 0h49m21s | price_call: R$ 4,77 | start_date_call: 2019-04-10 | start_time_call: 15:10:12"
    ]
}

```

# Deploy to Heroku

### Creating the Git repository in the project root folder

    apt-get update
    
    apt-get install git-core
    
    git init
    
### Creating the app at Heroku

You should install heroku CLI tools in your computer previously (See http://bit.ly/2jCgJYW)

    heroku apps:create app-name (Remember to grab the address of the app in this point)

### Setting the allowed hosts

include your address at the ALLOWED_HOSTS directives in settings.py - 
Just the domain, make sure that you will take the protocol and slashes from the string

### Heroku install config plugin

Sending configs from .env to Heroku ( You have to be inside tha folther where .env files is)

    heroku plugins:install heroku-config
    heroku config:push -a

To show heroku configs do

    heroku config
    
### Publishing the app

    git add .
    git commit -m 'Configuring the app'
    git push heroku master --force
    
### Creating the data base

    heroku run python3.6 manage.py migrate
    
### Creating the Django admin user

    heroku run python3 manage.py createsuperuser
