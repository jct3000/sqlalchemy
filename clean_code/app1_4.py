from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, orm, DateTime, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
# inclusao de classe geral de personal data
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative.api import DeclarativeMeta

from PersonalVerLibV2_2 import *
from DML import *
import sys

engine = create_engine('sqlite:///user.db', echo=True)                         # ('sqlite:///:memory:', echo=True)   --- coloca a BD em memoria  se mudar para algo tipo user.db cria em file na dir


#CHAMAR SEMPRE funcao de inicializacao da lib com o mesmo engine que a app
libInit(engine)



# Cria todas as tabelas e classes referentes a aplicacao
Base.metadata.create_all(bind=engine)






                                                    #Parte responsavel pela introducao dos objectos para a DB

Session = sessionmaker(bind=engine)

session= Session()


#recebe uma sessao e faz dump das classes na metatabela inicializando (meter a seguir a sessionmaker)
updatePersonnalClasses(session)

###############################################################################
# Introducao valores de testing-populating the BD
###############################################################################


person = Person(0,"joao", "hotmail" )
session.add(person)
session.commit()
person = Person(1,"miguel O VELHO", "gemail" )
#Muda data de validade
date=datetime(datetime.today().year,datetime.today().month, datetime.today().day,datetime.today().hour,datetime.today().minute,datetime.today().second)
person.created_date= date-timedelta(days=18000)
session.add(person)
session.commit()
person = Person(5,"miguel O SEGUNDO VELHO", "gemail900000" )
#Muda data de validade
date=datetime(datetime.today().year,datetime.today().month, datetime.today().day,datetime.today().hour,datetime.today().minute,datetime.today().second)
person.created_date= date-timedelta(days=18000)
session.add(person)
session.commit()
person = Person(2,"bruno", "hotmail2")
session.add(person)
session.commit()
person = Person(3,"Manuel", "hotmail45")
session.add(person)
session.commit()
person = Person(4,"Andre", "hotmail100")
session.add(person)
session.commit()
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

session.close()





###############################################################################
#  testes das funcoes da lib
###############################################################################



#ambas as funcoes tem de ter algo na BD
#teste do lista fora do prazo
print("\n\n\n\n\n  TESTES LISTA FORA PRAZO")
results=[]
results=clean_list(Person)
print("LISTA FORA VALIDADE:")
print(results)

#teste do show validade
teste=show_val(Person)
print("\n\n\n\n TESTES show_val: %d"%(teste))
#teste do show goal
teste=show_goal(Person)
print("\n\n\n\n TESTES show_goal: %s"%(teste))
#teste do show categorie
teste=show_categorie(Person)
print("\n\n\n\n TESTES show_categorie: %s"%(teste))
#teste do show owner
teste=show_data_owner(Person)
print("\n\n\n\n TESTES show_owner: %s"%(teste))
#teste do show source
teste=show_data_source(Person)
print("\n\n\n\n TESTES show_source: %s"%(teste))




#teste do limpa expired data
limpa(Person)

# change_goal(Checkin,None)
# change_categorie(Checkin,None)
# change_categorie(Person,None)
#teste do alerta_vazio
alerta_vazio()


#teste do change Metadados
change_val(Person,146)

#teste do show Metadados
teste=show_val(Person)
print("\n\n\n\n TESTES show_val: %d"%(teste))


#teste do change Metadados
change_val(Checkin,120)


change_goal(Checkin, "testegoal")
change_categorie(Checkin, "teste categoria")
change_data_owner(Checkin, "teste dono")
change_data_source(Checkin, "teste source")



#teste do show validade
teste=show_val(Checkin)
print("\n\n\n\n Checkin TESTES show_val: %d"%(teste))
#teste do show goal
teste=show_goal(Checkin)
print("\n\n\n\n Checkin TESTES show_goal: %s"%(teste))
#teste do show categorie
teste=show_categorie(Checkin)
print("\n\n\n\n Checkin TESTES show_categorie: %s"%(teste))
#teste do show owner
teste=show_data_owner(Checkin)
print("\n\n\n\n Checkin TESTES show_owner: %s"%(teste))
#teste do show source
teste=show_data_source(Checkin)
print("\n\n\n\n Checkin TESTES show_source: %s"%(teste))







is_private(Person)
is_private(Restaurant)
is_private(Checkin)




#ve as tabelas que tao na BD   APAGAR
print("\n\n\n\nTABELAS NA BD\n")
print (engine.table_names())
print(Person.__name__)
print("\n\n\n\nRELACOES NA BD")
#ve as ligacoes que tao na BD   APAGAR
#maneira 1
i=inspect(Person)
for relation in i.relationships:
    print(relation.direction.name)
    print(relation.remote_side)
    print(relation._reverse_property)
    #print as dos argumentos de relations
    #print(dir(relation))
#maneira 2
print("\n\n\n\nRELACOES NA BD man 2")
relationship_list = [str(list(column.remote_side)[0]).split('.')[0] for column in inspect(Person).relationships]
print (relationship_list)
print("TABELAS NA BD FIM\n\n\n\n\n")
print("\n\n\n\nPRIMARY KEY\n\n")
for key in inspect(Person).primary_key:
    print key.name



###############################################################################
#  print das tabelas
###############################################################################

                                                                            #parte responsavel pelo teste de query
Session = sessionmaker(bind=engine)
session= Session()



metas = session.query(Metatable).all()
for meta in metas:
    print ("\n\nTeste de metadados lista: %s proposito %s  categoria %s owner %s  origem  %s   validade %d  \n" %(meta.l_pessoal, meta.goal, meta.categorie, meta.data_owner, meta.data_source, meta.validade))



print("\n Persons data\n")
persons = session.query(Person).all()
for person in persons:
    print ("\n\nPessoa com o nome %s id %d e email %s    %s   || tag %s \n" %( person.name, person.id, person.email,person.created_date,person.personal_tag))

print("\n Restaurant data\n")
restaurants = session.query(Restaurant).all()
for restaurant in restaurants:
    print ("\n\nRestaurante com o nome %s id %d e a morada %s\n" %(restaurant.name, restaurant.id_r, restaurant.adress))


print("\nCheckin data\n")
checkins = session.query(Checkin).all()
for checkin in checkins:
    print ("\n\nTAG :%s ||||| checkin com o id %d da pessoa com id %d no restaurante de id %d Descricao %s e Qualificacao %d DATA CRIACAO:%s \n" %(checkin.personal_tag, checkin.id_c , checkin.id , checkin.id_r, checkin.description, checkin.rating,checkin.created_date))

session.close()


###############################################################################
#Print de testes
###############################################################################

print(type(Person))
print(isinstance(Checkin, PersonalData))
print("\nbases\n")
print(Restaurant.__bases__)
print("\n\n--------DESCENDENTES---------")
print(ordered_find_direct_descend(grafo, 'person'))

print("\n\n--------DESCENDENTES Publico---------")
print(ordered_find_direct_descend(grafo, 'restaurant'))

showclassdata(Person, 0)
#Testes dos modulos etc
#print(sys.modules["__main__"].__dict__["Person"])
#inspect.isclass(sys.modules["__main__"].__dict__["Person"])
