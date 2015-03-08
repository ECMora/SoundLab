# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey, String, Text, Boolean, Float, Date, func, and_
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from PyQt4.QtGui import QPixmap
import os


Base = declarative_base()

db_path = os.path.join(os.getcwd(), "utils", "db")
# db_path = "../../../utils/db"


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
    family = relationship(Family, backref='genres')

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
    genus = relationship(Genera, backref='species')

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
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    name = Column(Text(50), nullable=False)
    lastname = Column(Text(50), nullable=False)
    # endregion


class Parameter(Base):
    """
    The parameter of a measurement
    """

    # region CONSTANTS
    __tablename__ = 'Parameter'
    parameter_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    descp = Column(String(200))
    default_value = Column(Float(), nullable=False, default=0)
    # endregion

    def __eq__(self, other):
        return isinstance(other, Parameter) and self.name == other.name

    def __str__(self):
        return self.name


class ClassificationMethod(Base):
    """
    The parameter of a measurement
    """

    # region CONSTANTS
    __tablename__ = 'ClassificationMethod'
    method_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    descp = Column(String(200))
    # endregion

    def __eq__(self, other):
        return isinstance(other, ClassificationMethod) and self.name == other.name

    def __str__(self):
        return self.name


class Segment(Base):
    """
    The measurement of a parameter on a segment
    """

    # region CONSTANTS
    __tablename__ = 'Segment'
    segment_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    detection_date = Column(Date(), nullable=False, default=func.now())
    synchronized = Column(Boolean, nullable=True, default=False)

    user_id = Column(Integer, ForeignKey('User.user_id'), nullable=False, default=1)
    user = relationship(User, backref='segments_detected')

    identified_specie_id = Column(Integer, ForeignKey('Species.specie_id'))
    specie = relationship(Specie)

    identified_genus_id = Column(Integer, ForeignKey('Genera.genus_id'))
    genus = relationship(Genera)

    identified_family_id = Column(Integer, ForeignKey('Families.family_id'))
    family = relationship(Family)
    # endregion


class Measurement(Base):
    """
    The measurement of a parameter on a segment
    """

    # region CONSTANTS
    __tablename__ = 'Measurement'
    measurement_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    parameter_id = Column(Integer, ForeignKey('Parameter.parameter_id'), nullable=False)
    parameter = relationship(Parameter, backref='measurements')
    #                          ,cascade='delete, all')

    segment_id = Column(Integer, ForeignKey('Segment.segment_id'), nullable=False)
    segment = relationship(Segment, backref='measurements')\
    # , uselist=True,cascade='delete, all')

    value = Column(Float(), nullable=False, default=0)
    # endregion


class DB:

    db = create_engine('sqlite:///' + os.path.join(db_path, "duetto_local_db.s3db"))
    # db.echo = True
    db_session = orm.scoped_session(orm.sessionmaker(bind=db))


def clean_db():
    """
    removes the unidentified segments
    or those that have less than two measurments of the db
    :return:
    """
    session = DB.db_session
    useless_segments = session.query(Segment)

    # remove the unidentified and not measured segments
    for segment in useless_segments.all():
        if len(segment.measurements) < 2 or \
                (segment.specie is None and segment.genus is None and segment.family is None):
            for measure in segment.measurements:
                session.delete(measure)
            session.delete(segment)

    session.commit()