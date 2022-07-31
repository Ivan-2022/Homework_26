from sqlalchemy import Column, String, Integer, Float, ForeignKey

from project.setup.db import db, models


class Genre(models.Base):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)


class Director(models.Base):
    __tablename__ = 'directors'

    name = Column(String(100), unique=True, nullable=False)


class Movie(models.Base):
    __tablename__ = 'movies'

    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    trailer = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    genre_id = Column(Integer, ForeignKey(Genre.id), nullable=False)
    genre = db.relationship("Genre")
    director_id = Column(Integer, ForeignKey(Director.id), nullable=False)
    director = db.relationship("Director")


class User(models.Base):
    __tablename__ = 'users'
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255))
    surname = Column(String(255))
    favourite_genre = Column(String(255), ForeignKey(Genre.id))
    genre = db.relationship("Genre")
