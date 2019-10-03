from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, orm, DateTime, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
# inclusao de classe geral de personal data
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative.api import DeclarativeMeta


from PersonalVerLibV2_1 import *

###############################################################################
# DML- Data Manipulation Language
#
# Implementacao das classes pelo programador com vista a desenvolver a sua APP
###############################################################################

#########################
#Person
#
#PRIVATE CLASS-ROOT
############################
class Person (Base, PersonalData):
    #insert of metaclass
    __metaclass__ = CustomMetaClass


    #defining the sql tablename
    __tablename__ = 'person'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    email = Column ('email', String, unique=True)
    checkin_p=relationship("Checkin")

    def __repr__(self):
        return "<Person(name='%s', email='%s')>" % (self.name, self.email)

    def __init__(self, id, name, email):
        PersonalData.__init__(self)                             #tirar isto daqui????
        Base.__init__(self)
        self.id=id
        self.name=name
        self.email=email



#########################
#RESTAURANT
#
#PUBLIC CLASS-ROOT
############################
class Restaurant (Base):
    #insert of metaclass
    __metaclass__ = CustomMetaClass
    #defining the sql tablename
    __tablename__ = 'restaurant'

    id_r= Column('id_r', Integer, primary_key=True)
    name = Column('name', String)
    adress = Column ('adress', String, unique=True)
    checkin_r=relationship("Checkin")


    def __repr__(self):
        return "<Restaurant(name='%s', adress='%s')>" % (self.name, self.adress)

    def __init__(self, id, name, adress):
        self.id_r=id
        self.name=name
        self.adress=adress

#########################
#CHECKIN
#
#PRIVATE CLASS-LEAF
############################
class Checkin(Base ):
    #insert of metaclass
    __metaclass__ = CustomMetaClass
    #defining the sql tablename
    __tablename__ = 'checkin'

    id_c=Column('id_c', Integer, primary_key=True)
    id=Column(Integer, ForeignKey('person.id'))
    id_r= Column(Integer, ForeignKey('restaurant.id_r'))
    description = Column('description', String)
    rating = Column ('rating', Integer)


    def __repr__(self):
        return "<Checkin(description='%s', rating='%d')>" % (self.description, self.rating)

    def __init__(self, id_c, id, id_r, description, rating):
        self.id_c=id_c
        self.id=id
        self.id_r=id_r
        self.description=description
        self.rating=rating
