# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey, String, Text, Boolean
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from PyQt4.QtGui import QPixmap
import os


Base = declarative_base()
db_path = os.path.join(os.getcwd(), "Utils", "db")


class Family(Base):
    """
    The family of a specie
    """
    # region CONSTANTS
    __tablename__ = 'Families'
    family_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    # endregion

    def __eq__(self, other):
        return isinstance(other, Family) and self.name == other.name

    def __str__(self):
        return self.name


class Genera(Base):
    """
    The genre of a specie
    """
    # region CONSTANTS
    __tablename__ = 'Genera'
    genus_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    family_id = Column(Integer, ForeignKey('Families.family_id'), nullable=False)
    family = relationship(Family)
    name = Column(String(50), nullable=False)
    details = Column(Text(250), nullable=False)
    # endregion

    def __eq__(self, other):
        return isinstance(other, Genera) and self.name == other.name

    def __str__(self):
        return self.name


class Specie(Base):
    """
    An specie
    """

    # region CONSTANTS
    __tablename__ = 'Species'

    specie_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    genus_id = Column(Integer, ForeignKey('Genera.genus_id'), nullable=False)
    genus = relationship(Genera)
    picture = Column(String(50), nullable=True)
    name = Column(String(50), nullable=False)
    name_eng = Column(String(50), nullable=False)
    name_spa = Column(String(50), nullable=False)
    details = Column(String(250), nullable=True)
    endemic = Column(Boolean, nullable=True)

    # endregion
    def __eq__(self, other):
        return isinstance(other, Specie) and self.name == other.name

    def __str__(self):
        return self.name_spa + " (" + self.name + ")"

    @property
    def image(self):
        if not self.picture:
            return None

        return QPixmap(os.path.join(db_path, "pictures", self.picture))

    @property
    def image_url(self):
        return None if not self.picture else os.path.join(db_path, "pictures", self.picture)


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


def get_db_session():
    """
    Gets a session to query against the db
    :return:
    """
    db = create_engine('sqlite:///' + os.path.join(db_path, "duetto_local_db.s3db"))
    session = orm.scoped_session(orm.sessionmaker(bind=db))
    return session
