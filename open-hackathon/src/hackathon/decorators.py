from flask import g
from functools import wraps
from user import user_manager
from admin.admin_mgr import admin_manager
from log import log


def role_required(*roles):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if len(roles) == 0:
                return func(*args, **kwargs)
            else:
                return g.user.is_authenticated() and g.user.has_roles(*roles) and func(*args, **kwargs)

        return decorated_view

    return wrapper


def token_required(func):
    def authenticate_and_call(*args, **kwargs):
        if not user_manager.validate_request():
            return "Access Denied", 403
        return func(*args, **kwargs)

    return authenticate_and_call


def admin_token_required(func):
    def authenticate_and_call(*args, **kwargs):
        if not admin_manager.validate_request():
            return "Access Denied", 403
        return func(*args, **kwargs)

    return authenticate_and_call


def admin_hackathon_authority_check(func):
    def authenticate_and_call(*args, **kwargs):
        if not admin_manager.check_admin_hackathon_authority():
            return "Access Denied", 403
        return func(*args, **kwargs)

    return authenticate_and_call
