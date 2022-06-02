from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec import FlaskApiSpec
import mongoengine
import traceback
from app.controller.dashBoardController import DashBoardController
from app.controller.noticeController import NoticeController
from app.controller.userController import UserController
from app.controller.myPageController import MyPageController


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config.update(
        {
            "APISPEC_SPEC": APISpec(
                title="Title",
                version="1.0.0",
                openapi_version="3.0.0",
                plugins=[MarshmallowPlugin()],
            ),
            "APISPEC_SWAGGER_URL": "/swagger-json/",
            "APISPEC_SWAGGER_UI_URL": "/swagger/",
        }
    )
    doc = FlaskApiSpec(app)
    # doc.register(UserController)
    try:
        mongoengine.connect(host="mongodb://localhost:27017/aimmo_ojt")
        print("connect database success")
    except Exception as e:
        traceback.print_exc()
        print("connect database error:" + e)

    UserController.register(app)
    NoticeController.register(app)
    DashBoardController.register(app)
    MyPageController.register(app)

    return app
