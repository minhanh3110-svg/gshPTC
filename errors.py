from flask import Blueprint, render_template, jsonify, request
from werkzeug.exceptions import HTTPException

errors = Blueprint('errors', __name__)

class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@errors.app_errorhandler(404)
def not_found_error(error):
    if request.path.startswith('/api/'):
        return jsonify(error="Không tìm thấy tài nguyên"), 404
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(500)
def internal_error(error):
    if request.path.startswith('/api/'):
        return jsonify(error="Lỗi máy chủ nội bộ"), 500
    return render_template('errors/500.html'), 500

@errors.app_errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code

@errors.app_errorhandler(HTTPException)
def handle_exception(e):
    """Xử lý tất cả các lỗi HTTP khác"""
    if request.path.startswith('/api/'):
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }).data
        response.content_type = "application/json"
        return response
    return render_template(f'errors/{e.code}.html'), e.code 