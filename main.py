from flask import Flask
from flask_classful import FlaskView, route
from flask_restx import Api

from controller.dashBoardController import DashBoardController
from controller.noticeController import NoticeController
from controller.userController import UserController
from controller.myPageController import MyPageController

app = Flask(__name__)
api = Api(app, version="1.0", title="게시판 Api", description="API description")
app.config.SWAGGER_UI_DOC_EXPANSION = "full"


class Main(FlaskView):
    @route("/test")
    def home(self):
        return "welcome"


Main.register(app)
UserController.register(app)
NoticeController.register(app)
DashBoardController.register(app)
MyPageController.register(app)

if __name__ == "__main__":
    app.run("127.0.0.1", port=8080, debug=True)
