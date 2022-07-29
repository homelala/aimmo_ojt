from flask import Blueprint, jsonify
from flask_apispec import marshal_with
from flask_swagger_ui import get_swaggerui_blueprint

from app.view.user import UserView
from app.view.notice import NoticeView
from app.view.my_page import MyPageView
from app.view.dash_board import DashBoardView
from app.errors import ApiError, ApiErrorSchema

api = Blueprint("api", __name__)


def register_api(app):
    UserView.register(api)
    NoticeView.register(api)
    MyPageView.register(api)
    DashBoardView.register(api)

    register_swagger(api)
    app.register_blueprint(api)

    SWAGGER_URL = '/api-docs'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = '/apispec'  # Our API url (can of course be a local resource)

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Test application"
        },
    )

    app.register_blueprint(swaggerui_blueprint)
    register_error_handler(app)


def register_swagger(bp):
    from app.utils.apidocs_utils import generate_api_spec

    @bp.route("/apispec")
    def apispec():
        return jsonify(generate_api_spec(title="aimmo-ojt", version="v1", bp_name=bp.name if isinstance(bp, Blueprint) else None))

def register_error_handler(bp):
    bp.register_error_handler(ApiError, handle_api_error)

@marshal_with(ApiErrorSchema())
def handle_api_error(e: ApiError):
    return e, e.status_code