from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec import FlaskApiSpec
import mongoengine
import traceback
import os
from app.view.dashBoardController import DashBoardController
from app.view.noticeController import NoticeController
from app.view.userView import UserView
from app.view.myPageController import MyPageController
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

    from flask_cors import CORS

    CORS(app, resources={r"*": {"origins": "*"}})

    UserView.register(app)
    NoticeController.register(app)
    DashBoardController.register(app)
    MyPageController.register(app)

    return app
