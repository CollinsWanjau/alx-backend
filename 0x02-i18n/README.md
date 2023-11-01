# 0x02. i18n

## Learning Objectives

- Learn how to parametrize Flask templates to display different languages
- Learn how to infer the correct locale based on URL parameters, user settings or request headers
- Learn how to localize timestamps

# Tasks

## 0. Basic Flask app

File: [0-app.py](0-app.py/) - [0-app.py](0-app.py/)

First you will setup a basic Flask app in 0-app.py. Create a single / route and an index.html template that simply outputs “Welcome to Holberton” as page title (<title>) and “Hello world” as header (<h1>).

## 1. Basic Babel setup

File: [1-app.py](1-app.py/) - [1-app.py](1-app.py/)

Install the Babel Flask extension:

```
pip3 install flask_babel
```

Then instantiate the Babel object in your app. Store it in a module-level variable named babel.

In order to configure available languages in our app, you will create a Config class that has a LANGUAGES class attribute equal to ["en", "fr"].

Use Config to set Babel’s default locale ("en") and timezone ("UTC").

Use that class as config for your Flask app.

## 2. Get locale from request

File: [2-app.py](2-app.py/) - [2-app.py](2-app.py/)

Create a get_locale function with the babel.localeselector decorator. Use request.accept_languages to determine the best match with our supported languages.

## 3. Parametrize templates

File: [3-app.py](3-app.py/) - [3-app.py](3-app.py/)

Use the _ or gettext function to parametrize your templates. Use the message IDs home_title and home_header.

Create a babel.cfg file containing

```
[python: **.py]
[jinja2: **/templates/**.html]
extensions=jinja2.ext.autoescape,jinja2.ext.with_
```

Then initialize your translations with
    
```
pybabel extract -F babel.cfg -o messages.pot .
```

and your two dictionaries with

```
$ pybabel init -i messages.pot -d translations -l en
$ pybabel init -i messages.pot -d translations -l fr
```

Then edit files translations/[en|fr]/LC_MESSAGES/messages.po to provide the correct value for each message ID for each language. Use the following translations:

msgid	English	French
home_title	"Welcome to Holberton"	"Bienvenue chez Holberton"
home_header	"Hello world!"	"Bonjour monde!"

Finally compile your dictionaries with

```
pybabel compile -d translations
```

Reload the home page of your app and make sure that the correct messages show up.
## 4. Force locale with URL parameter