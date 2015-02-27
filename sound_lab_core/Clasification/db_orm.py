# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey, String, Text, Boolean
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


Base = declarative_base()


class Specie(Base):
    """
    An specie
    """

    # region CONSTANTS
    __tablename__ = 'Species'

    specie_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    genus_id = Column(Integer, nullable=False, autoincrement=True)
    picture = Column(String(50), nullable=True)
    name = Column(String(50), nullable=False)
    name_eng = Column(String(50), nullable=False)
    name_spa = Column(String(50), nullable=False)
    details = Column(String(250), nullable=True)
    status = Column(Integer, nullable=True)
    endemic = Column(Boolean, nullable=True)

    # endregion


class Family(Base):
    """
    The family of a specie
    """
    # region CONSTANTS
    __tablename__ = 'Families'
    family_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    details = Column(String(250), nullable=False)
    # endregion


class Genera(Base):
    """
    The genre of a specie
    """
    # region CONSTANTS
    __tablename__ = 'Genera'
    genus_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    family_id = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)
    details = Column(Text(250), nullable=False)
    # endregion


class User(Base):
    """
    The picture of a specie
    """
    # region CONSTANTS
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    name = Column(Text(50), nullable=False)
    lastname = Column(Text(50), nullable=False)
    # endregion


#
# class Address(Base):
# __tablename__ = 'address'
# # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     street_name = Column(String(250))
#     street_number = Column(String(250))
#     post_code = Column(String(250), nullable=False)
#     person_id = Column(Integer, ForeignKey('person.id'))
#     person = relationship(Person)


db = create_engine('sqlite:///db/duetto_local_db.s3db')

sm = orm.sessionmaker(bind=db)
session = orm.scoped_session(sm)

q = session.query(Specie)
for r in q.limit(50):
    print r.name
