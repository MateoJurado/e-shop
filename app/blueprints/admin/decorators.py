<<<<<<< HEAD
from functools import wraps
from flask import abort
from flask_login import current_user

def admin_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.es_admin():
            abort(403)          # Prohibido
        return f(*args, **kwargs)
=======
from functools import wraps
from flask import abort
from flask_login import current_user

def admin_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.es_admin():
            abort(403)          # Prohibido
        return f(*args, **kwargs)
>>>>>>> f7d16a8be16f03e7db395170a45e982b073714e8
    return decorated_function