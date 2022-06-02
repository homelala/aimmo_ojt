import traceback

from utils import CustomException
from app.utils.ErrorResponseDto import ErrorResponseDto


def errorHandler(app):
    @app.errorHandler(Exception)
    def error_handler(e):
        traceback.print_exc()
        return ErrorResponseDto("서버 상에서 오류가 발생했습니다.", 500)

    @app.errorhandler(AttributeError)
    def handle_error(e):
        traceback.print_exc()
        return ErrorResponseDto("서버 상에서 오류가 발생했습니다.", 500)

    @app.errorhandler(KeyError)
    def handle_key_error(e):
        traceback.print_exc()
        return ErrorResponseDto("데이터베이스에서 값을 가져오는데 문제가 발생하였습니다.", 500)

    @app.errorhandler(TypeError)
    def handle_type_error(e):
        traceback.print_exc()
        return ErrorResponseDto("데이터의 값이 잘못 입력되었습니다", 500)

    @app.errorhandler(ValueError)
    def handle_value_error(e):
        traceback.print_exc()
        return ErrorResponseDto("데이터에 잘못된 값이 입력되었습니다.", 500)

    @app.errorhandler(CustomException)
    def custom_error(e):
        traceback.print_exc()
        return ErrorResponseDto(e.error_message, e.status_code).toJSON()
