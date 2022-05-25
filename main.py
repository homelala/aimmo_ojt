from flask import Flask
from flask_restx import Api
import mongoengine
import traceback
from controller.dashBoardController import DashBoardController
from controller.noticeController import NoticeController
from controller.userController import UserController
from controller.myPageController import MyPageController


class CreateApp:
    app = Flask(__name__)
    api = Api(app, version="1.0", title="게시판 Api", description="API description")
    app.config.SWAGGER_UI_DOC_EXPANSION = "full"

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
