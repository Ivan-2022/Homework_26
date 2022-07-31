from flask import request
from flask_restx import Namespace, Resource
from project.container import user_service
from project.setup.api.models import user

api = Namespace('user')


@api.route('/')
class UserView(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def get(self):
        """
        Возвращает информацию о пользователе (его профиль).
        """
        header = request.headers['Authorization'].split("Bearer ")[-1]
        return user_service.get_user_by_token(refresh_token=header)

    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def patch(self):
        """
        Изменяет информацию пользователя (имя, фамилия, любимый жанр)
        """
        data = request.json
        header = request.headers['Authorization'].split("Bearer ")[-1]
        return user_service.update_user(data=data, refresh_token=header)


@api.route('/password/')
class UserView(Resource):
    """
    Обновляет пароль пользователя.
    """
    def put(self):
        data = request.json
        header = request.headers['Authorization'].split("Bearer ")[-1]
        return user_service.update_password(data=data, refresh_token=header)
