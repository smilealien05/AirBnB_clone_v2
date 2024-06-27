#!/usr/bin/python3
"""Define storage engine using MySQL database
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{db}', pool_pre_ping=True)
        
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        all_objs = {}
        if cls:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = f'{cls.__name__}.{obj.id}'
                all_objs[key] = obj
        else:
            classes = [User, State, City, Amenity, Place, Review]
            for cls in classes:
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = f'{cls.__name__}.{obj.id}'
                    all_objs[key] = obj
        return all_objs

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)
