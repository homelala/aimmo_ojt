from app.repository import noticeCommentRepository, noticeRepository


def get_my_articles(user_id):
    notice = noticeRepository.find_by_user_id(user_id)
    return notice


def get_my_comment(user_id):
    notice = noticeCommentRepository.find_by_user_id(user_id)
    return notice
