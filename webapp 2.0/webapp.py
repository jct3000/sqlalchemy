#sqlalchemy imports
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, orm, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
# inclusao de classe geral de personal data
from sqlalchemy.ext.declarative import declared_attr

#Lib imports
from PersonalVerLibV2 import *

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
    chekin_p=relationship("Checkin")

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
    schedule_r=relationship("Schedule")

    def __repr__(self):
        return "<Restaurant(name='%s', adress='%s')>" % (self.name, self.adress)

    def __init__(self, id, name, adress):
        self.id_r=id
        self.name=name
        self.adress=adress


class Checkin(Base, PersonalData):
    __tablename__ = 'checkin'

    id_c=Column('id_c', Integer, primary_key=True)
    id=Column(Integer, ForeignKey('person.id'))
    id_r= Column(Integer, ForeignKey('restaurant.id_r'))
    description = Column('description', String)
    rating = Column ('rating', Integer)
    grade_c=relationship("Grade")

    def __repr__(self):
        return "<Checkin(description='%s', rating='%d')>" % (self.description, self.rating)

    def __init__(self, id_c, id, id_r, description, rating):
        PersonalData.__init__(self)                             #Parte de inicializacao da lib
        self.id_c=id_c
        self.id=id
        self.id_r=id_r
        self.description=description
        self.rating=rating

class Employee (Base, PersonalData):        #, PersonalData
    __tablename__ = 'employee'

    id_e = Column('id_e', Integer, primary_key=True)
    name = Column('name', String)
    email = Column ('email', String, unique=True)
    schedule_e=relationship("Schedule")

    def __repr__(self):
        return "<Person(name='%s', email='%s')>" % (self.name, self.email)

    def __init__(self, id_e, name, email):
        PersonalData.__init__(self)                             #Parte de inicializacao da lib
        self.id_e=id_e
        self.name=name
        self.email=email


class Schedule (Base, PersonalData):
    __tablename__ = 'schedule'

    id_s=Column('id_s', Integer, primary_key=True)
    id_e=Column(Integer, ForeignKey('employee.id_e'))
    id_r= Column(Integer, ForeignKey('restaurant.id_r'))
    checkin= Column ('checkin', DateTime)
    checkout= Column ('checkout', DateTime)
    grade_s=relationship("Grade")

    def __repr__(self):
        return "<Schedule(checkin='%s', checkout='%s')>" % (self.checkin, self.checkout)

    def __init__(self, id_s, id_e, id_r, checkin,checkout):
        PersonalData.__init__(self)                             #Parte de inicializacao da lib
        self.id_s=id_s
        self.id_e=id_e
        self.id_r=id_r
        self.checkin=checkin
        self.checkout=checkout

class Grade (Base, PersonalData):
    __tablename__ = 'grade'

    id_g=Column('id_g', Integer, primary_key=True)
    id_s=Column(Integer, ForeignKey('schedule.id_s'))
    id_c= Column(Integer, ForeignKey('checkin.id_c'))
    grade = Column('grade', Integer)


    # def __repr__(self):
    #    return "<Grade(grade='%d')>" % (self.grade)

    def __init__(self, id_g, id_s, id_c, grade):
        PersonalData.__init__(self)                             #Parte de inicializacao da lib
        self.id_g=id_g
        self.id_s=id_s
        self.id_c=id_c
        self.grade=grade


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

@route('/newemployee')#pagina inscrever novo empregado
def newemployee():
    return template('new_employee')

@route('/newcheckin/<id>')#pagina inscrever novo checkin de um id
def newcheckin(id):
    return template('new_checkin',id=id)

@route('/new_grade/<id_c>')#pagina inscrever nova avalicao de um id
def newgrade(id_c):
    return template('grade_form',id_c=id_c)






@route('/employee_checkin/<id_e>/<id_s>/<id_r>')#pagina checkin de empregado
def employee_checkin(id_e,id_s,id_r):
    Session = sessionmaker(bind=engine)
    session= Session()
    schedule = Schedule(id_s,id_e,id_r,datetime.now().replace(microsecond=0),datetime.now().replace(microsecond=0))   #queria meter None no checkout mas isso da problemas no showall com o isoformat mas grava NULL se n meter nda
    session.add(schedule)                                                                                              # neste caso se n fizer checkout fica com a data de checkin
    session.commit()
    session.close()
    return '<h1>Go to work Id:{0} at restaurant :{1} Schedule: {2}</h1>'.format(id_e, id_r,id_s) #template('new_checkin',id_e=id_e, id_s=id_s,id_r=id_r)

@route('/employee_checkout/<id_e>/<id_s>/<id_r>')#pagina checkout de empregado
def employee_checkout(id_e,id_s,id_r):
    Session = sessionmaker(bind=engine)
    session= Session()
    value=datetime.now().replace(microsecond=0) + timedelta(hours=8)
    session.query(Schedule).filter(Schedule.id_s==id_s).update({Schedule.checkout:value}, synchronize_session=False)
    session.commit()
    session.close()
    return '<h1>Work Done of Employee Id:{0} at restaurant :{1} Schedule: {2} is Over</h1>'.format(id_e, id_r,id_s) #template('new_checkin',id_e=id_e, id_s=id_s,id_r=id_r)







@route('/deleteperson/<id>')#pagina apagar dados de uma pessoa de id
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

@route('/signinemployee') # log in de empregado
def signinperson():
    return template('employee_id_form')

@route('/signinrestaurant') # log in de restaurant
def signinperson():
    return template('restaurant_id_form')







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

@post('/doform_employee') #formulario de novo empregado
def process3():

    name = request.forms.get('name')
    id_e = request.forms.get('id_e')
    email = request.forms.get('email')
    Session = sessionmaker(bind=engine)
    session= Session()
    employee = Employee(id_e,name, email )
    session.add(employee)
    session.commit()
    session.close()
    return template('stored_person', name=name, id=id_e, email=email)

@post('/doform_id')   #formulario de log in pessoa
def processid():
    id = request.forms.get('id')
    return template('id_person', id=id)#'<h1>Id Page</h1>'

@post('/doform_id_restaurant')   #formulario de log in restaurant
def processid():
    id_r = request.forms.get('id_r')
    return template('id_restaurant', id_r=id_r)#'<h1>Id Page</h1>'

@post('/doform_id_employee')   #formulario de log in empregado
def processidemployee():
    id_e = request.forms.get('id_e')
    id_s = request.forms.get('id_s')
    id_r = request.forms.get('id_r')
    return template('id_employee', id_e=id_e, id_s=id_s, id_r=id_r)#'<h1>Id Page</h1>'

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


@post('/new_grade/doform_grade') #formulario de nova avaliacao
def processgrade():
    id_c = request.forms.get('id_c')
    id_s = request.forms.get('id_s')
    id_g = request.forms.get('id_g')
    value = request.forms.get('grade')
    Session = sessionmaker(bind=engine)
    session= Session()
    grade = Grade(id_g,id_s,id_c, value )
    session.add(grade)
    session.commit()
    session.close()
    return template('stored_grade', id_c=id_c, id_s=id_s, id_g=id_g, value=value)










@route('/showcheckin/<id>') #get???   show de dados pessoais de visitas de um id
def showcheckin(id):
    Session = sessionmaker(bind=engine)
    session= Session()
    checkins = session.query(Checkin).filter(Checkin.id==id)
    results4=[]
    for checkin in checkins:
        results4.append({'id':checkin.id_c,'restaurant_id':checkin.id_r,'person_id':checkin.id,'description':checkin.description,'rating':checkin.rating,'Personal_tag':checkin.personal_tag,'creation_date':checkin.created_date.isoformat()})  # data n funciona em jason
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

####################################################################################################
# HIDE THE QUERIES FROM PROGRAMATOR
###################################################################################################


@route('/show_data_person/<id>') #get???   show de dados pessoais de um id
def showperson(id):
    results5=showclassdata(Person, id)
    return {'Personal Data': results5}#'<h1>Personal Page of id  {0}</h1>'.format(id)


####################################################################################################

@route('/showrestaurant/<id_r>') #get???   show de dados pessoais de um id restaurant
def showrestaurant(id_r):
    Session = sessionmaker(bind=engine)
    session= Session()
    restaurants = session.query(Restaurant).filter(Restaurant.id_r==id_r)
    results_show_restaurants=[]
    for restaurant in restaurants:
        results_show_restaurants.append({'id':restaurant.id_r,'name':restaurant.name,'adress':restaurant.adress, })
    #session.close()
    return {'Restaurant Data': results_show_restaurants}

@route('/showschedules_r/<id_r>') #get???   show de schedules de um id restaurant
def showschedule(id_r):
    Session = sessionmaker(bind=engine)
    session= Session()
    schedules = session.query(Schedule).filter(Schedule.id_r==id_r)
    results_show_schedules=[]
    for schedule in schedules:
        results_show_schedules.append({'Schedule_id':schedule.id_s,'Employee_Id':schedule.id_e,'Restaurant_Id':schedule.id_r,'Checkin_date':schedule.checkin.isoformat(),'Checkout_date':schedule.checkout.isoformat(), 'Personal_tag':schedule.personal_tag,'creation_date':schedule.created_date.isoformat()})  # data n funciona em jason
    #session.close()
    return {'Schedules Data': results_show_schedules}



@route('/showgrade_r/<id_r>') #get???   show de grades de um id restaurant
def showgrade(id_r):
    Session = sessionmaker(bind=engine)
    session= Session()
    schedules = session.query(Schedule).filter(Schedule.id_r==id_r)
    results_show_grades=[]
    for schedule in schedules:
        grades = session.query(Grade).filter(Grade.id_s==schedule.id_s)
        for grade in grades:
            results_show_grades.append({'Grade id':grade.id_g,'Schedule Id':grade.id_s,'Checkin Id':grade.id_c, 'Grade': grade.grade, 'Personal_tag':grade.personal_tag,'creation_date':grade.created_date.isoformat()})  # data n funciona em jason
    #session.close()
    return {'Grades Data': results_show_grades}


@route('/showemployee/<id_e>') #get???   show de dados pessoais de um id empregado
def showperson(id_e):
    Session = sessionmaker(bind=engine)
    session= Session()
    employees = session.query(Employee).filter(Employee.id_e==id_e)
    results_p_employee=[]
    for employee in employees:
        results_p_employee.append({'Employee id':employee.id_e,'name':employee.name,'email':employee.email, 'Personal_tag':employee.personal_tag,'creation_date':employee.created_date.isoformat()})  # data n funciona em jason
    #session.close()
    return {'Employee Personal Data': results_p_employee}













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
        results3.append({'id':checkin.id_c,'restaurant_id':checkin.id_r,'person_id':checkin.id,'description':checkin.description,'rating':checkin.rating, 'Personal_tag':checkin.personal_tag,'creation_date':checkin.created_date.isoformat()})  # 'Personal_tag':person.personal_tag,'creation_date':person.created_date.isoformat() data n funciona em jason
    employees = session.query(Employee).all()
    resultsemployee=[]
    for employee in employees:
        resultsemployee.append({'Employee id':employee.id_e,'name':employee.name,'email':employee.email, 'Personal_tag':employee.personal_tag,'creation_date':employee.created_date.isoformat()})  # data n funciona em jason
    schedules = session.query(Schedule).all()
    results_schedule=[]
    for schedule in schedules:
        results_schedule.append({'Schedule_id':schedule.id_s,'Employee_Id':schedule.id_e,'Restaurant_Id':schedule.id_r,'Checkin_date':schedule.checkin.isoformat(),'Checkout_date':schedule.checkout.isoformat(), 'Personal_tag':schedule.personal_tag,'creation_date':schedule.created_date.isoformat()})  # data n funciona em jason
    grades = session.query(Grade).all()
    results_grade=[]
    for grade in grades:
        results_grade.append({'Grade id':grade.id_g,'Schedule Id':grade.id_s,'Checkin Id':grade.id_c, 'Grade': grade.grade, 'Personal_tag':grade.personal_tag,'creation_date':grade.created_date.isoformat()})
    #session.close()
    return{'Persons Data': results, 'Restaurants Data': results2,'Checkins Data': results3, 'Employees Data': resultsemployee,'Schedules Data':results_schedule ,'Grades Data':results_grade}





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
    return "Time constrain of the class person is {0} days".format(result)

#   TEM DE TER ALGUMA PESSOA NA TABELA
# nao sera melhor nao depender da classe??
@route('/cleanperson')   # limpa dados pessoais fora de validade
def cleanperson():
    limpa(Person) #mudar nome???
    return '<h1>Person Class all within expiration date</h1>'

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
    #person.personal_tag=1
    #Muda data de validade
    date=datetime(datetime.today().year,datetime.today().month, datetime.today().day,datetime.today().hour,datetime.today().minute,datetime.today().second)
    person.created_date= date-timedelta(days=18000)
    session.add(person)
    session.commit()
    person = Person(35,"miguel O SEGUNDO VELHO", "gemail900000" )
    #person.personal_tag=1
    #Muda data de validade
    date=datetime(datetime.today().year,datetime.today().month, datetime.today().day,datetime.today().hour,datetime.today().minute,datetime.today().second)
    person.created_date= date-timedelta(days=18000)
    session.add(person)
    session.commit()
    person = Person(32,"bruno", "hotmail2")
    session.add(person)
    session.commit()
    person = Person(34,"Andre", "hotmail100")
    session.add(person)
    session.commit()
    person = Person(33,"Manuel", "hotmail45")
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
    employee = Employee(40,"trabalhador1", "sapo")
    session.add(employee)
    session.commit()
    employee = Employee(41,"trabalhador2", "sapo2")
    session.add(employee)
    session.commit()
    employee = Employee(42,"trabalhador VELHO", "sapo900000" )
    #employee.personal_tag=1
    #Muda data de validade
    date=datetime(datetime.today().year,datetime.today().month, datetime.today().day,datetime.today().hour,datetime.today().minute,datetime.today().second)
    employee.created_date= date-timedelta(days=18000)
    session.add(employee)
    session.commit()
    schedule = Schedule(40,40,31,datetime.now().replace(microsecond=0)+timedelta(hours=1),datetime.now().replace(microsecond=0)+timedelta(hours=8))
    session.add(schedule)#id_s, id_e, id_r, checkin,checkout
    session.commit()
    schedule = Schedule(41,41,32,datetime.now().replace(microsecond=0)+timedelta(hours=2),datetime.now().replace(microsecond=0)+timedelta(hours=8))
    session.add(schedule)
    session.commit()
    schedule = Schedule(42,42,32,datetime.now().replace(microsecond=0)+timedelta(hours=1),datetime.now().replace(microsecond=0)+timedelta(hours=4))
    session.add(schedule)
    session.commit()
    grade = Grade(40,42,30, 99 )  #id_g, id_s, id_c, grade
    session.add(grade)
    session.commit()
    grade = Grade(41,41,31, 999 )
    session.add(grade)
    session.commit()
    session.close()
    return '<h1>Creating Done</h1>'

                                                            #FIM funcao de testes de intro na BD APAGAR


if __name__=='__main__':
    run(debug=True, reloader=True)
