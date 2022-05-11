from flask import Flask, Blueprint

from controller import userController

app = Flask(__name__)
app.register_blueprint(userController.userApp, url_prefix="/user")


@app.route("/")
def home():
    return "welcome"


if __name__ == "__main__":
    app.run("127.0.0.1", port=8080, debug=True)
