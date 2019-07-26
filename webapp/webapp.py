#sqlalchemy imports
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, orm, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
# inclusao de classe geral de personal data
from sqlalchemy.ext.declarative import declared_attr

#Lib imports

#bottle imports
from bottle import run, route, template, post , request, get

#data Base creation
engine = create_engine('sqlite:///user.db', echo=True)


Base=declarative_base()   # tirar devido a lib init da biblioteca




class Person (Base):        #, PersonalData
    __tablename__ = 'person'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    email = Column ('email', String, unique=True)
    #chekin_p=relationship("Checkin")

    def __repr__(self):
        return "<Person(name='%s', email='%s')>" % (self.name, self.email)

    def __init__(self, id, name, email):
        #PersonalData.__init__(self)                             #Parte de inicializacao da lib
        self.id=id
        self.name=name
        self.email=email

Base.metadata.create_all(bind=engine)






                                                                #Parte do Bottle
@route('/')
def index():
    return template('index')#'<h1>Index Page</h1>'




@route('/client')
def client():
    return template('client')#'<h1>Client Page</h1>'

@post('/doform')
def process():

    name = request.forms.get('name')
    id = request.forms.get('id')
    email = request.forms.get('email')
    Session = sessionmaker(bind=engine)
    session= Session()
    person = Person(id,name, email )
    session.add(person)
    session.commit()
    session.close()
    return template('stored', name=name, id=id, email=email)                                                 #"Your name is {0} id :{1} email: {2}".format(name, id,email)


@get('/showall')
def showall():
    Session = sessionmaker(bind=engine)
    session= Session()
    persons = session.query(Person).all()
    results=[]
    for person in persons:
        results.append({'id':person.id,'name':person.name,'email':person.email})
    #session.close()
    return{'Persons Data': results}

@route('/admin')
def admin():
    return '<h1>Administrator Page</h1>'



if __name__=='__main__':
    run(debug=True, reloader=True)
