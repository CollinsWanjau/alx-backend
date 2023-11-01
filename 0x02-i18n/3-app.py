#!/usr/bin/env python3
""" Basic Babel setup
"""


from flask import Flask, render_template, request
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


@babel.localeselector
def get_locale():
    """Determine the best match with supported languages

    Returns:
            _type_: _description_
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])

# babel.init_app(app, locale_selector=get_locale)

@app.route('/')
def hello_world():
    """_summary_
    """
    return render_template('3-index.html')


if __name__ == '__main__':
    app.run(port='5000', host='0.0.0.0', debug=True)
