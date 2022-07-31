import calendar
import datetime
from flask import abort, current_app

import jwt

from project.tools.security import compare_password_hash


def generate_tokens(email, password, password_hash=None, is_refresh=False):
    if email is None:
        raise abort(404)
    if not is_refresh:
        if not compare_password_hash(password_hash=password_hash, password=password):
            abort(400)

    data = {"email": email,
            "password": password}
    min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
    data["exp"] = calendar.timegm(min15.timetuple())
    access_token = jwt.encode(data, key=current_app.config['SECRET_KEY'], algorithm=current_app.config['ALGORITHM'])

    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, key=current_app.config['SECRET_KEY'], algorithm=current_app.config['ALGORITHM'])

    return {"access_token": access_token, "refresh_token": refresh_token}


def approve_refresh_token(refresh_token):
    data = jwt.decode(jwt=refresh_token, key=current_app.config['SECRET_KEY'],
                      algorithms=current_app.config['ALGORITHM'])
    email = data.get("email")
    password = data.get("password")
    return generate_tokens(email, password, is_refresh=True)


def get_data_from_token(refresh_token):
    try:
        data = jwt.decode(jwt=refresh_token, key=current_app.config['SECRET_KEY'],
                          algorithms=current_app.config['ALGORITHM'])
        return data
    except Exception:
        return None
