from flask import Blueprint
from CTFd.plugins import register_plugin_assets_directory
from .routes import start_challenge_api

def load(app):
    app.register_blueprint(start_challenge_api)