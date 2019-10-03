#sqlalchemy imports
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, orm, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
# inclusao de classe geral de personal data
from sqlalchemy.ext.declarative import declared_attr

#Lib imports
from PersonalVerLib import *

#bottle imports
from bottle import run, route, template, post , request, get

#data Base creation
engine = create_engine('sqlite:///user.db', echo=True)

#CHAMAR SEMPRE funcao de inicializacao da lib com o mesmo engine que a app
libInit(engine)
#Base=declarative_base()   # tirar devido a lib init da biblioteca




class Person (Base, PersonalData):        #, PersonalData
    __tablename__ = 'person'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    email = Column ('email', String, unique=True)
    #chekin_p=relationship("Checkin")

    def __repr__(self):
        return "<Person(name='%s', email='%s')>" % (self.name, self.email)

    def __init__(self, id, name, email):
        PersonalData.__init__(self)                             #Parte de inicializacao da lib
        self.id=id
        self.name=name
        self.email=email

class Restaurant (Base):
    __tablename__ = 'restaurant'

    id_r= Column('id_r', Integer, primary_key=True)
    name = Column('name', String)
    adress = Column ('adress', String, unique=True)
    chekin_r=relationship("Checkin")

    def __repr__(self):
        return "<Restaurant(name='%s', adress='%s')>" % (self.name, self.adress)

    def __init__(self, id, name, adress):
        self.id_r=id
        self.name=name
        self.adress=adress


class Checkin(Base):
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


Base.metadata.create_all(bind=engine)




                                                                # Parte de testes APAGAR





                                                                #Parte do Bottle
@route('/')#pagina index
def index():
    return template('index')#'<h1>Index Page</h1>'




@route('/client')#pagina clientes / restaurantes
def client():
    return template('client')

@route('/newperson')#pagina inscrever nova pessoa
def newclient():
    return template('new_person')

@route('/newrestaurant')#pagina inscrever nova restaurante
def newrestaurant():
    return template('new_restaurant')

@route('/newcheckin/<id>')#pagina inscrever novo checkin de um id
def newrestaurant(id):
    return template('new_checkin',id=id)

@route('/deleteperson/<id>')#pagina apagar dados de um id
def deleteperson(id):
    Session = sessionmaker(bind=engine)
    session= Session()
    persons = session.query(Person).filter(Person.id==id).delete()
    session.commit()
    session.close()
    return template('delete_person',id=id)

@route('/signinperson') # log in de pessoa
def signinperson():
    return template('person_id_form')

                                                                        #funcao de testes de intro na BD APAGAR
@route('/create')
def create():
    #Da erro a meter directamente na base de dados
    Session = sessionmaker(bind=engine)
    # para deixar o campo a nulo usar None
    session= Session()
    person = Person(30,"joao", "hotmail" )
    #person.personal_tag=1
    session.add(person)
    session.commit()
    person = Person(31,"miguel O VELHO", "gemail" )
    person.personal_tag=1
    #Muda data de validade
    date=datetime(datetime.today().year,datetime.today().month, datetime.today().day,datetime.today().hour,datetime.today().minute,datetime.today().second)
    person.created_date= date-timedelta(days=18000)
    session.add(person)
    session.commit()
    person = Person(35,"miguel O SEGUNDO VELHO", "gemail900000" )
    person.personal_tag=1
    #Muda data de validade
    date=datetime(datetime.today().year,datetime.today().month, datetime.today().day,datetime.today().hour,datetime.today().minute,datetime.today().second)
    person.created_date= date-timedelta(days=18000)
    session.add(person)
    session.commit()
    person = Person(32,"bruno", "hotmail2")
    session.add(person)
    session.commit()
    person = Person(33,"Manuel", "hotmail45")
    session.add(person)
    session.commit()
    person = Person(34,"Andre", "hotmail100")
    session.add(person)
    session.commit()
    restaurant = Restaurant(31,"Dinner","street" )
    session.add(restaurant)
    session.commit()
    restaurant = Restaurant(33,"MAC","Lisboa" )
    session.add(restaurant)
    session.commit()
    restaurant = Restaurant(32,"Pizza","Benfica" )
    session.add(restaurant)
    session.commit()
    checkin = Checkin(30,31 , 30 , "blabla", 3)
    session.add(checkin)
    session.commit()
    checkin = Checkin(31,32 , 33 , "blabla2", 7)
    session.add(checkin)
    session.commit()
    session.close()
    return '<h1>Creating Done</h1>'

                                                                #FIM funcao de testes de intro na BD APAGAR





@post('/doform_person') #formulario de nova pessoa
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
    return template('stored_person', name=name, id=id, email=email)                                                 #"Your name is {0} id :{1} email: {2}".format(name, id,email)

@post('/doform_restaurant') #formulario de novo restaurante
def process2():

    name = request.forms.get('name')
    id = request.forms.get('id')
    adress = request.forms.get('adress')
    Session = sessionmaker(bind=engine)
    session= Session()
    restaurant = Restaurant(id,name, adress )
    session.add(restaurant)
    session.commit()
    session.close()
    return template('stored_restaurant', name=name, id=id, adress=adress)                                                 #"Your name is {0} id :{1} email: {2}".format(name, id,email)

@post('/doform_id')   #formulario de log in
def processid():
    id = request.forms.get('id')
    return template('id_person', id=id)#'<h1>Id Page</h1>'

@post('/newcheckin/doform_checkin')   #formulario new checkin   WHY /newcheckin/???? NAO PERCEBI TENTAR MUDAR
def processcheckin():
    id_c = request.forms.get('id_c')
    id = request.forms.get('id')
    id_r = request.forms.get('id_r')
    description = request.forms.get('description')
    rating = request.forms.get('rating')
    Session = sessionmaker(bind=engine)
    session= Session()
    checkin = Checkin(id_c, id, id_r, description, rating)
    session.add(checkin)
    session.commit()
    session.close()
    return template('stored_checkin', id=id, id_c=id_c, id_r=id_r, description=description, rating=rating)#'<h1>Id Page</h1>'


@route('/showcheckin/<id>') #get???   show de dados pessoais de visitas de um id
def showcheckin(id):
    Session = sessionmaker(bind=engine)
    session= Session()
    checkins = session.query(Checkin).filter(Checkin.id==id)
    results4=[]
    for checkin in checkins:
        results4.append({'id':checkin.id_c,'restaurant_id':checkin.id_r,'person_id':checkin.id,'description':checkin.description,'rating':checkin.rating})  # data n funciona em jason
    #session.close()
    return {'Checkins of person': results4}#'<h1>Personal Page of id  {0}</h1>'.format(id)



@route('/showperson/<id>') #get???   show de dados pessoais de um id
def showperson(id):
    Session = sessionmaker(bind=engine)
    session= Session()
    persons = session.query(Person).filter(Person.id==id)
    results5=[]
    for person in persons:
        results5.append({'id':person.id,'name':person.name,'email':person.email, 'Personal_tag':person.personal_tag,'creation_date':person.created_date.isoformat()})  # data n funciona em jason
    #session.close()
    return {'Personal Data': results5}#'<h1>Personal Page of id  {0}</h1>'.format(id)



@route('/admin')   # pagina de admin
def admin():
    return template('admin')#'<h1>Administrator Page</h1>'

@get('/showall')   #admin show all
def showall():
    Session = sessionmaker(bind=engine)
    session= Session()
    persons = session.query(Person).all()
    results=[]
    for person in persons:
        results.append({'id':person.id,'name':person.name,'email':person.email, 'Personal_tag':person.personal_tag,'creation_date':person.created_date.isoformat()})  # data n funciona em jason
    restaurants = session.query(Restaurant).all()
    results2=[]
    for restaurant in restaurants:
        results2.append({'id':restaurant.id_r,'name':restaurant.name,'adress':restaurant.adress, })  # 'Personal_tag':person.personal_tag,'creation_date':person.created_date.isoformat() data n funciona em jason
    checkins = session.query(Checkin).all()
    results3=[]
    for checkin in checkins:
        results3.append({'id':checkin.id_c,'restaurant_id':checkin.id_r,'person_id':checkin.id,'description':checkin.description,'rating':checkin.rating })  # 'Personal_tag':person.personal_tag,'creation_date':person.created_date.isoformat() data n funciona em jason
    #session.close()
    return{'Persons Data': results, 'Restaurants Data': results2,'Checkins Data': results3}



#   TEM DE TER ALGUMA PESSOA NA TABELA
@route('/listcleanperson')   # lista dados pessoais fora de validade
def liscleanperson():
    results6=[]
    results6=clean_list(Person)
    return {'Persons Data Expired': results6}

#   TEM DE TER ALGUMA PESSOA NA TABELA
@route('/showval')   # lista dados pessoais fora de validade
def showval():
    result=show_val(Person)
    return "Time constrain of the class person is {0}".format(result)

#   TEM DE TER ALGUMA PESSOA NA TABELA
# nao sera melhor nao depender da classe??
@route('/cleanperson')   # limpa dados pessoais fora de validade
def cleanperson():
    limpa(Person) #mudar nome???
    return '<h1>Person Class all within expiration date</h1>'

if __name__=='__main__':
    run(debug=True, reloader=True)
