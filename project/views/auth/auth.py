from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.setup.api.models import user

api = Namespace('auth')


@api.route('/register/')
class AuthsView(Resource):
    @api.marshal_with(user, as_list=True, code=201, description='OK')
    def post(self):
        """
        Передавая  email и пароль, создаем пользователя в системе
        """
        req_json = request.json
        email = req_json.get("email")
        password = req_json.get("password")
        if not (email or password):
            return "", 400
        else:
            return user_service.create_new_user(email, password)


@api.route('/login/')
class AuthView(Resource):
    @api.response(404, 'Not Found')
    def post(self):
        """
        Передаем email и пароль и, если пользователь прошел аутентификацию, возвращаем пользователю
        "access_token" и "refresh_token".
        """
        req_json = request.json
        email = req_json.get("email")
        password = req_json.get("password")
        if not (email or password):
            return "", 400
        else:
            return user_service.compare_password(email, password), 201

    @api.response(404, 'Not Found')
    def put(self):
        """
        Принимаем пару токенов и, если они валидны, создаем пару новых
        """
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        if not refresh_token:
            return "", 400
        else:
            return user_service.update_token(refresh_token), 201
