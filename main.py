from flask import Flask
from flask_classful import FlaskView, route
from flask_restx import Api, Resource
from controller.userController import UserController

app = Flask(__name__)
# app.register_blueprint(userController.userApp, url_prefix="/user")
api = Api(app, version="1.0", title="게시판 Api", description="API description")


class Main(FlaskView):
    @route("/test")
    def home(self):
        return "welcome"


Main.register(app)
UserController.register(app)

if __name__ == "__main__":
    app.run("127.0.0.1", port=8080, debug=True)
