import os
import traceback

import mongoengine
from flask import Flask

import app.config as config
from app.view import register_api
from app.view.dash_board import DashBoardView
from app.view.my_page import MyPageView
from app.view.notice import NoticeView
from app.view.user import UserView


def create_app():
    app = Flask(__name__)
    app.debug = True
    config_name = os.getenv("APP_ENV") or "dev"

    try:
        app.config.from_object(config.config_by_name[config_name])
        mongoengine.connect(host=app.config["MONGO_URI"])

        print("connect database success")
    except Exception as e:
        traceback.print_exc()
        print("connect database error:" + str(e))

    register_api(app)

    return app
