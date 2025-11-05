from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404) #type: ignore
def error_404(error: int) -> tuple[str, int]:
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403) #type: ignore
def error_403(error: int) -> tuple[str, int]:
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500) #type: ignore
def error_500(error: int) -> tuple[str, int]:
    return render_template('errors/500.html'), 500

