from flask import abort
from typing import Optional

from project.dao.user import UsersDAO
from project.exceptions import ItemNotFound
from project.models import User
from project.services.auths_service import generate_tokens, approve_refresh_token, get_data_from_token
from project.tools.security import generate_password_hash


class UsersService:
    def __init__(self, dao: UsersDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> list[User]:
        return self.dao.get_all(page=page)

    def create_new_user(self, login, password):
        self.dao.create(login, password)

    def get_user_by_login(self, login):
        return self.dao.get_user_by_login(login)

    def compare_password(self, login, password):
        user = self.get_user_by_login(login)
        return generate_tokens(email=user.email, password=password, password_hash=user.password)

    def update_token(self, refresh_token):
        return approve_refresh_token(refresh_token)

    def get_user_by_token(self, refresh_token):
        data = get_data_from_token(refresh_token)
        if data:
            email = data.get("email")
            return self.get_user_by_login(email)

    def update_user(self, data: dict, refresh_token):
        user = self.get_user_by_token(refresh_token)
        if user:
            self.dao.update(login=user.email, data=data)
            return self.get_user_by_token(refresh_token)

    def update_password(self, data, refresh_token):
        user = self.get_user_by_token(refresh_token)
        current_password = data.get('old_password')
        if not current_password:
            abort(400)
        new_password = data.get('new_password')
        self.dao.update(login=user.email, data={"password": generate_password_hash(new_password)})
        return self.compare_password(login=user.email, password=data.get('new_password'))
