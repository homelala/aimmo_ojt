from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
import mongoengine
import traceback
import os
from app.view.dash_board import DashBoardView
from app.view.notice import NoticeView
from app.view.user import UserView
from app.view.my_page import MyPageView
import sys
import app.config as config


def create_app():
    app = Flask(__name__)
    app.debug = True
    config_name = os.getenv("APP_ENV") or "dev"
    # app.config.update(
    #     {
    #         "APISPEC_SPEC": APISpec(
    #             title="Title",
    #             version="1.0.0",
    #             openapi_version="3.0.0",
    #             plugins=[MarshmallowPlugin()],
    #         ),
    #         "APISPEC_SWAGGER_URL": "/swagger-json/",
    #         "APISPEC_SWAGGER_UI_URL": "/swagger/",
    #     }
    # )
    # doc = FlaskApiSpec(app)

    try:
        app.config.from_object(config.config_by_name[config_name])
        mongoengine.connect(host=app.config["MONGO_URI"])

        print("connect database success")
    except Exception as e:
        traceback.print_exc()
        print("connect database error:" + str(e))

    UserView.register(app)
    DashBoardView.register(app)
    MyPageView.register(app)
    NoticeView.register(app)

    return app
