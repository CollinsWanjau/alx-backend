#!/usr/bin/env python3
""" Basic Babel setup
"""


from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config(object):
    """Configure available langauges in your app with config class

    Returns:
            _type_: _description_
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# CONFIGURE the flask app
app = Flask(__name__)
# configure the app using a configuration object
app.config.from_object(Config)
# instantiate babel object and store it in a module-level variable
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """ returns a user dictionary or None if the ID cannot be found
    """
    login_id = request.args.get('login_as')
    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request():
    """Before request"""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Determine the best match with supported languages

    Returns:
            _type_: _description_
    """
    # check if the locale query parameter is present and if its value is in the
    # list of supported languages.
    if 'locale' in request.args and request.args.get('locale') in
    app.config['LANGUAGES']:
        return request.args.get('locale')
    # we check if g.user is not None and if the user's preferred locale is in
    # the list of supported languages.
    elif g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')
    else:
        return request.accept_languages.best_match(app.config['LANGUAGES'])


# babel.init_app(app, locale_selector=get_locale)


@app.route('/')
def hello_world():
    """_summary_
    """
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run(port='5000', host='0.0.0.0', debug=True)
