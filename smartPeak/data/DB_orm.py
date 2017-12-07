# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DB_orm():
    def __init__(self):
        self.engine = None
        self.Session = None

    def make_engineFromSettings(self, settings_I={}):
        '''make the database engine

        Aargs:
            settings_I (dict): a dictionary of settings e.g., settings name:settings value

        '''
        engine = create_engine("postgresql://%s:%s@%s/%s" % (
            settings_I['user'], settings_I['password'], 
            settings_I['host'], settings_I['database']))
        self.engine = engine
        return engine

    def make_engine(
        self, 
        database_I='',
        user_I='',
        password_I='',
        host_I="localhost:5432"
    ):
        '''make the database engine'''
        engine = create_engine("postgresql://%s:%s@%s/%s" % (
            user_I, password_I, host_I, database_I))
        self.engine = engine
        return engine

    def make_defaultEngine(self):
        '''return default database engine'''
        engine = create_engine("postgres://postgres@/postgres")
        self.engine = engine
        return engine

    def make_connectionFromSettings(
        self,
        settings_I={}
    ):
        '''return connection to the database
        '''
        try:
            engine = self.make_engineFromSettings(settings_I)
            conn = engine.connect()
            conn.execute("commit")
            return conn
        except SQLAlchemyError as e:
            print(e)
            exit(-1)

    def make_connection(
        self,
        database_I='postgres',
        user_I='postgres',
        password_I='postgres',
        host_I="localhost:5432"
    ):
        '''return connection to the database
        '''
        try:
            engine = self.make_engine(
                database_I=database_I,
                user_I=user_I,
                password_I=password_I,
                host_I=host_I)
            conn = engine.connect()
            conn.execute("commit")
            return conn
        except SQLAlchemyError as e:
            print(e)
            exit(-1)

    def get_connection(self):
        '''return connection to the database
        '''
        try:
            conn = self.engine.connect()
            conn.execute("commit")
            return conn
        except SQLAlchemyError as e:
            print(e)
            exit(-1)

    def set_sessionFromSettings(self, settings_I):
        '''set a session object'''
        engine = self.make_engineFromSettings(settings_I)
        self.Session = sessionmaker(bind=engine)

    def set_session(
        self,
        engine_I=None,
        database_I='',
        user_I='',
        password_I='',
        host_I="localhost:5432"
    ):
        '''set a session object
        '''
        if engine_I:
            self.Session = sessionmaker(bind=engine_I)
        else:
            engine = self.make_engine(
                database_I=database_I,
                user_I=user_I,
                password_I=password_I,
                host_I=host_I)
            self.Session = sessionmaker(bind=engine)        

    def get_session(self):
        '''return new session object'''
        session = self.Session()
        return session 

    def get_engine(self):
        '''return engine'''
        return self.engine 