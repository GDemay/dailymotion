# -*- coding: utf-8 -*-
# DBへの接続設定
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
 
user_name = "user"
password = "password"
host = "db"
database_name = "sample_db"

DATABASE = 'mysql://%s:%s@%s/%s?charset=utf8' % (
    user_name,
    password,
    host,
    database_name,
)

ENGINE = create_engine(
    DATABASE,
    encoding="utf-8",
    echo=True
)

Session = sessionmaker(bind=ENGINE)

scoped_session = scoped_session(Session)
session = Session()

Base = declarative_base()

