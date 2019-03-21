from flask import Flask
from codeStatic.account import account
from codeStatic.home import home


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.DevConfig')
    app.register_blueprint(account)
    app.register_blueprint(home)

    return app
