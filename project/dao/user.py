from project.dao.base import BaseDAO
from project.models import User
from project.tools.security import generate_password_hash
from project.setup.db import db


class UsersDAO(BaseDAO[User]):
    __model__ = User

    def create(self, login, password):
        new_user = User(email=login, password=generate_password_hash(password))
        self._db_session.add(new_user)
        self._db_session.commit()

    def get_user_by_login(self, login):
        return db.session.query(self.__model__).filter(self.__model__.email == login).one()

    def update(self, login, data):
        db.session.query(self.__model__).filter(self.__model__.email == login).update(data)

        self._db_session.commit()
