from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec import doc, FlaskApiSpec
import mongoengine
import traceback
from controller.dashBoardController import DashBoardController
from controller.noticeController import NoticeController
from controller.userController import UserController
from controller.myPageController import MyPageController


class CreateApp:
    app = Flask(__name__)
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

    if __name__ == "__main__":
        app.run("127.0.0.1", port=8080, debug=True)
