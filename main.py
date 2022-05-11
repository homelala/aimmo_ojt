from flask import Flask
from flask_restx import Api, Resource
from controller import userController

app = Flask(__name__)
app.register_blueprint(userController.userApp, url_prefix="/user")
api = Api(app, version="1.0", title="게시판 Api", description="API description")


@app.route("/test")
def home():
    return "welcome"


if __name__ == "__main__":
    app.run("127.0.0.1", port=8080, debug=True)
