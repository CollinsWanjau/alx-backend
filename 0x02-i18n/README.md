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

# localeselector

- The Babel instance provides a `localeselector` decorator that can be used to mark functions as callables for selecting the best matching locale for a user. The function is passed the list of locales that are supported by the application and should return one of them.

```python
from flask import request

# ...

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])
```

- Here we are using an attr of flask's `request` object called `accept_languages`.This object provides a best_match() method that takes a list of languages and returns the best match for the user, based on the Accept-Language header. The best match is determined using the following algorithm:

```
For each requested language, find the best match in the list of supported languages. The best match is the language with the highest quality and, if two languages have the same quality, the one with the highest order in the list of supported languages is chosen.
If no match is found, the best match is the first language in the list of requested languages.
```

- The best_match() method returns a language tag, which is a string in the format languagecode2-country/regioncode2. For example, the language tag for English as spoken in the United States is en-US. The language tag for French as spoken in Canada is fr-CA.

- The best_match() method also has a fallback argument, which is used if no match is found. The default value for this argument is *, which means that the first language in the list of requested languages is returned if no match is found. You can also pass None as the fallback value, which means that None is returned if no match is found.

- In case you are curious, here is an example of a complex Accept-Language header:

```
Accept-Language: da, en-gb;q=0.8, en;q=0.7
```

- This header means that the client prefers Danish, but will accept British English and other types of English. The quality value is used to indicate the relative preference for each language. The quality value is a number between 0 and 1, where 1 is the highest preference. The default quality value is 1, so en-gb;q=0.8 means that British English is preferred over other types of English.

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

### Marking Texts to Translate in Python Source Code

- The first step in the translation process is to mark all texts that should be translated in the source code. This is done by wrapping the texts in a call to the gettext() function. The gettext() function is imported from the flask_babel module.

- The gettext() function takes a single argument, which is the text to translate. The function returns a string that is the translation of the text. The translation is based on the language that is currently active. If no translation is available for the text, the original text is returned.

- The way texts are marked for translation is by wrapping them in a function call that as a convention is called `_()`.

```python
from flask_babel import _
# ...
flash(_('Your post is now live!'))
```

- The idea is that the _() function wraps the text in the base langauge (English) This function will use the language selected by the `get_locale()` function to return the correct translation.

- There is an even harder case to handle. Some strings literals are assigned outside of a request context, usually when the app is starting up The only solution to handle this problem is to handle those texts is to find a way to delay the evaluation of the string literal until the request context is available. This can be done by wrapping the string literal in a lazy string. A lazy string is a special object that represents a string literal, but doesn’t evaluate it until it is used in a context where the request context is available. The lazy string is created by calling the lazy_gettext() function, which is imported from the flask_babel module.

```python
from flask_babel import lazy_gettext as _l

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    # ...
```

### Marking Texts to Translate in Jinja2 Templates

- The gettext() function is also available in Jinja2 templates. The function is imported from the flask_babel package and is available as _.

- For example, consider the following template:

```html
<h1>File not Found</h1>
```

- The translation enabled verison becomes:

```html
<h1>{{ _('File not Found')}}</h1>
```

### Exctraction of Texts to Translate

- You can use the `pybabel` command to extract them to a .pot file, which stands for `portable object template`. This file contains all the texts that should be translated. The .pot file is a template for the .po files, which are the files that contain the actual translations.

- The purpose of this file is to server as a template to create translation files for each language.

- The extraction process needs a small configuration file that tells pybabel what files should be scanned for translatable texts. The configuration file is called `babel.cfg` and should be placed in the root directory of the project.

- The babel.cfg file should contain the following:

```babel.cfg
[python: **.py]
[jinja2: **/templates/**.html]
extensions=jinja2.ext.autoescape,jinja2.ext.with_
```

- The first two lines define the filename patterns for Python and Jinja2 template files respectively. The third line specifies the Jinja2 extensions that should be loaded when parsing the templates. The autoescape extension is needed to properly handle HTML escaping. The with_ extension is needed to support the with statement in Jinja2 templates.

- The extraction process is started by running the pybabel extract command. The command takes the following arguments:

```
pybabel extract -F babel.cfg -k _l -o messages.pot .
```

- The -F option specifies the name of the configuration file. The -k option specifies the name of the function that is used to mark texts for translation. The -o option specifies the name of the output file. The last argument is the directory that should be scanned for translatable texts. The . argument means that the current directory should be scanned.

- The output of the pybabel extract command is a file called messages.pot. This file contains all the texts that should be translated. The file is called a template because it is used as a template to create the .po files, which are the files that contain the actual translations.

## 4. Force locale with URL parameter



