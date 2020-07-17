from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, orm, DateTime, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
# inclusao de classe geral de personal data
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative.api import DeclarativeMeta

from PersonalVerLibV2_4 import *

import sys

engine = create_engine('sqlite:///user.db', echo=True)                         # ('sqlite:///:memory:', echo=True)   --- coloca a BD em memoria  se mudar para algo tipo user.db cria em file na dir


#CHAMAR SEMPRE funcao de inicializacao da lib com o mesmo engine que a app
libInit(engine)



class Person (Base, PersonalData):
    #introducao de metaclass
    __metaclass__ = CustomMetaClass
    __tablename__ = 'person'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    email = Column ('email', String, unique=True)
    checkin_p=relationship("Checkin")

    # def __repr__(self):
    #     return "<Person(id='%s',name='%s', email='%s')>" % (self.id,self.name, self.email)          tirei isto pk do list clean em objectos WHY???


    def __init__(self, id, name, email):
        #PersonalData.__init__(self)                             #tirar isto daqui????
        #Base.__init__(self)
        self.id=id
        self.name=name
        self.email=email




class Restaurant (Base):
    __tablename__ = 'restaurant'
    __metaclass__ = CustomMetaClass

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


class Checkin(Base ):
    #introducao de metaclass
    __metaclass__ = CustomMetaClass
    __tablename__ = 'checkin'

    id_c=Column('id_c', Integer, primary_key=True)
    id=Column(Integer, ForeignKey('person.id'))
    id_r= Column(Integer, ForeignKey('restaurant.id_r'))
    description = Column('description', String)
    rating = Column ('rating', Integer)

    #para ter algo nas ligacoes do inspect
    # num= relationship("Restaurant", back_populates="checkin_r")
    # num2=relationship("Person", back_populates="checkin_p")


    def __repr__(self):
        return "<Checkin(description='%s', rating='%d')>" % (self.description, self.rating)

    def __init__(self, id_c, id, id_r, description, rating):
#        PersonalData.__init__(self)
        self.id_c=id_c
        self.id=id
        self.id_r=id_r
        self.description=description
        self.rating=rating


class Grade (Base):
        #introducao de metaclass
    __metaclass__ = CustomMetaClass
    __tablename__ = 'grade'

    id_g=Column('id_g', Integer, primary_key=True)
    id_c= Column(Integer, ForeignKey('checkin.id_c'))
    grade = Column('grade', Integer)


    # def __repr__(self):
    #    return "<Grade(grade='%d')>" % (self.grade)

    def __init__(self, id_g, id_c, grade):                           #Parte de inicializacao da lib
        self.id_g=id_g
        self.id_c=id_c
        self.grade=grade


# class Teste (Base):
#         #introducao de metaclass
#     __metaclass__ = CustomMetaClass
#     __tablename__ = 'teste'
#
#     id_t=Column('id_t', Integer, primary_key=True)
#     id_g= Column(Integer, ForeignKey('grade.id_g'))
#     number = Column('number', Integer)
#
#
#     # def __repr__(self):
#     #    return "<Grade(grade='%d')>" % (self.grade)
#
#     def __init__(self, id_t, id_g, number):                           #Parte de inicializacao da lib
#         self.id_t=id_t
#         self.id_g=id_g
#         self.number=number

###############################################################################
# Mudar a base em runtime
###############################################################################


#Checkin.__bases__ = Checkin.__bases__ + (PersonalData,)


###############################################################################

# Cria todas as tabelas e classes referentes a aplicacao
Base.metadata.create_all(bind=engine)






                                                    #Parte responsavel pela introducao dos objectos para a DB

Session = sessionmaker(bind=engine)

session= Session()


#recebe uma sessao e faz dump das classes na metatabela inicializando (meter a seguir a sessionmaker)
updatePersonnalClasses(session)

###############################################################################
# Introducao valores de testing
###############################################################################


session= Session()
start_time = datetime.now()
max=10
i=0
filler=bytearray(1000)
print("HERE\n")
print(filler)
print(len(filler))
a=sys.getsizeof(filler)
print(a)
while i<max :
    person = Person(i,"joao"+str(i), "hotmail"+str(filler)+str(i) )
    session.add(person)
    session.commit()
    i=i+1

session.close()
end_time = datetime.now()
#teste de funcao que adiciona uma pessoa
#adder()


# person = Person(1,"miguel O VELHO", "gemail" )
# #person.personal_tag=1
# #Muda data de validade
# date=datetime(datetime.today().year,datetime.today().month, datetime.today().day,datetime.today().hour,datetime.today().minute,datetime.today().second)
# person.created_date= date-timedelta(days=18000)
#
# session.add(person)
# session.commit()
#
# person = Person(5,"miguel O SEGUNDO VELHO", "gemail900000" )
# #person.personal_tag=1
# #Muda data de validade
# date=datetime(datetime.today().year,datetime.today().month, datetime.today().day,datetime.today().hour,datetime.today().minute,datetime.today().second)
# person.created_date= date-timedelta(days=18000)
#
# session.add(person)
# session.commit()
#
# person = Person(2,"bruno", "hotmail2")
# session.add(person)
# session.commit()
#
# person = Person(3,"Manuel", "hotmail45")
# session.add(person)
# session.commit()
#
# person = Person(4,"Andre", "hotmail100")
# session.add(person)
# session.commit()

# session.query(Person).filter(Person.id==0).delete()                           # Para apagar um objecto com querie
# session.commit()                                                              # Para apagar um objecto com querie

restaurant = Restaurant(1,"Dinner","street" )
session.add(restaurant)
session.commit()

restaurant = Restaurant(3,"MAC","Lisboa" )
session.add(restaurant)
session.commit()

restaurant = Restaurant(2,"Pizza","Benfica" )
session.add(restaurant)
session.commit()

checkin = Checkin(0,1 , 0 , "blabla", 3)
session.add(checkin)
session.commit()

checkin = Checkin(2,0 , 0 , "teste", 2)
session.add(checkin)
session.commit()

checkin = Checkin(3,0 , 0 , "teste222", 99)
session.add(checkin)
session.commit()

checkin = Checkin(1,2 , 3 , "blabla2", 7)
session.add(checkin)
session.commit()

grade=Grade(1, 3, 1111)
session.add(grade)
session.commit()

grade=Grade(2, 2, 22222)
session.add(grade)
session.commit()

grade=Grade(3, 2, 3333)
session.add(grade)
session.commit()

grade=Grade(4, 1, 9)
session.add(grade)
session.commit()
#Funcao de update de um valor o synchronize_session pode ter o valor 'evaluate'
# session.query(Restaurant).filter(Restaurant.adress == "street").update({Restaurant.adress: "street2"}, synchronize_session=False)
# session.commit()



# teste=Teste(1, 2, 7777)
# session.add(teste)
# session.commit()
#
#
# teste=Teste(2, 4, 0000)
# session.add(teste)
# session.commit()

session.close()





###############################################################################
#  testes das funcoes da lib
###############################################################################

#
#
# #ambas as funcoes tem de ter algo na BD
# #teste do lista fora do prazo
# print("\n\n\n\n\n  TESTES LISTA FORA PRAZO")
# results=[]
# results=clean_list(Person)
# print("LISTA FORA VALIDADE:")
# print(results)
#
# #teste do show validade
# teste=show_val(Person)
# print("\n\n\n\n TESTES show_val: %d"%(teste))
# #teste do show goal
# teste=show_goal(Person)
# print("\n\n\n\n TESTES show_goal: %s"%(teste))
# #teste do show categorie
# teste=show_categorie(Person)
# print("\n\n\n\n TESTES show_categorie: %s"%(teste))
# #teste do show owner
# teste=show_data_owner(Person)
# print("\n\n\n\n TESTES show_owner: %s"%(teste))
# #teste do show source
# teste=show_data_source(Person)
# print("\n\n\n\n TESTES show_source: %s"%(teste))
#
#
#
# print("\n\n\nclean list\n\n")
# p=clean_list(Person)
# print p
#
# print("\n\n\nclean listOBJECTOS\n\n")
# p=clean_list_obj(Person)
# print p
# #teste do limpa expired data
# limpa(Person)
# print("\nclean list after\n\n")
# p=clean_list(Person)
# print p
# # change_goal(Checkin,None)
# # change_categorie(Checkin,None)
# # change_categorie(Person,None)
# #teste do alerta_vazio
# alerta_vazio()
#
#
# #teste do change Metadados
# change_val(Person,146)
#
# #teste do show Metadados
# teste=show_val(Person)
# print("\n\n\n\n TESTES show_val: %d"%(teste))
#
#
# #teste do change Metadados
# change_val(Checkin,120)
#
#
# change_goal(Checkin, "testegoal")
# change_categorie(Checkin, "teste categoria")
# change_data_owner(Checkin, "teste dono")
# change_data_source(Checkin, "teste source")
#
#
#
# #teste do show validade
# teste=show_val(Checkin)
# print("\n\n\n\n Checkin TESTES show_val: %d"%(teste))
# #teste do show goal
# teste=show_goal(Checkin)
# print("\n\n\n\n Checkin TESTES show_goal: %s"%(teste))
# #teste do show categorie
# teste=show_categorie(Checkin)
# print("\n\n\n\n Checkin TESTES show_categorie: %s"%(teste))
# #teste do show owner
# teste=show_data_owner(Checkin)
# print("\n\n\n\n Checkin TESTES show_owner: %s"%(teste))
# #teste do show source
# teste=show_data_source(Checkin)
# print("\n\n\n\n Checkin TESTES show_source: %s"%(teste))
#
#
#
#
#
#
#
# is_private(Person)
# is_private(Restaurant)
# is_private(Checkin)
#
#
#
#
# #ve as tabelas que tao na BD   APAGAR
# print("\n\n\n\nTABELAS NA BD\n")
# print (engine.table_names())
# print(Person.__name__)
# print("\n\n\n\nRELACOES NA BD")
# #ve as ligacoes que tao na BD   APAGAR
# #maneira 1
# i=inspect(Person)
# for relation in i.relationships:
#     print(relation.direction.name)
#     print(relation.remote_side)
#     print(relation._reverse_property)
#     #print as dos argumentos de relations
#     #print(dir(relation))
# #maneira 2
# print("\n\n\n\nRELACOES NA BD man 2")
# relationship_list = [str(list(column.remote_side)[0]).split('.')[0] for column in inspect(Person).relationships]
# print (relationship_list)
# print("TABELAS NA BD FIM\n\n\n\n\n")
# print("\n\n\n\nPRIMARY KEY\n\n")
# for key in inspect(Person).primary_key:
#     print key.name
#


###############################################################################
#  print das tabelas
###############################################################################

                                                                            #parte responsavel pelo teste de query
Session = sessionmaker(bind=engine)
session= Session()



# metas = session.query(Metatable).all()
# for meta in metas:
#     print ("\n\nTeste de metadados lista: %s proposito %s  categoria %s owner %s  origem  %s   validade %d  \n" %(meta.l_pessoal, meta.goal, meta.categorie, meta.data_owner, meta.data_source, meta.validade))
#
# roots = session.query(Roots).all()
# for meta in roots:
#     print ("\n\nTeste de metadados_roots lista: %s "%(meta.l_pessoal))
#
print("\n Persons data\n")
persons = session.query(Person).all()
for person in persons:
    print ("\n\nPessoa com o nome %s id %d e email %s    %s   || tag %s \n" %( person.name, person.id, person.email,person.created_date,person.personal_tag))

# print("\n Restaurant data\n")
# restaurants = session.query(Restaurant).all()
# for restaurant in restaurants:
#     print ("\n\nRestaurante com o nome %s id %d e a morada %s\n" %(restaurant.name, restaurant.id_r, restaurant.adress))
#
#
# print("\nCheckin data\n")
# checkins = session.query(Checkin).all()
# for checkin in checkins:
#     print ("\n\nTAG :%s ||||| checkin com o id %d da pessoa com id %d no restaurante de id %d Descricao %s e Qualificacao %d DATA CRIACAO:%s \n" %(checkin.personal_tag, checkin.id_c , checkin.id , checkin.id_r, checkin.description, checkin.rating,checkin.created_date))

session.close()


###############################################################################
#Print de testes
###############################################################################
#
# print(type(Person))
# print(isinstance(Checkin, PersonalData))
# print("\nbases\n")
# print(Restaurant.__bases__)
# print("\n\n--------DESCENDENTES---------")
# print(ordered_find_direct_descend(grafo, 'person'))
#
# print("\n\n--------DESCENDENTES Publico---------")
# print(ordered_find_direct_descend(grafo, 'restaurant'))
#
# showclassdata(Person, 0)
#
#
# print("showdata obj")
# p=showclassdata_obj(Person, 0)
# print("\n\nshowdata obj second print\n\n")
# print p
# print rootClasses
# #Testes dos modulos etc
# #print(sys.modules["__main__"].__dict__["Person"])
# #inspect.isclass(sys.modules["__main__"].__dict__["Person"])
print('Duration: {}'.format(end_time - start_time))
