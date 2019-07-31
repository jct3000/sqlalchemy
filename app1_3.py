from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, orm, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
# inclusao de classe geral de personal data
from sqlalchemy.ext.declarative import declared_attr


from PersonalVerLib import *



engine = create_engine('sqlite:///user.db', echo=True)                         # ('sqlite:///:memory:', echo=True)   --- coloca a BD em memoria  se mudar para algo tipo user.db cria em file na dir


#CHAMAR SEMPRE funcao de inicializacao da lib com o mesmo engine que a app
libInit(engine)



class Person (Base, PersonalData ):
    __tablename__ = 'person'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    email = Column ('email', String, unique=True)
    chekin_p=relationship("Checkin")

    def __repr__(self):
        return "<Person(name='%s', email='%s')>" % (self.name, self.email)

    def __init__(self, id, name, email):
        PersonalData.__init__(self)                             #tirar isto daqui????
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




# Cria todas as tabelas e classes referentes a aplicacao
Base.metadata.create_all(bind=engine)






                                                    #Parte responsavel pela introducao dos objectos para a DB

Session = sessionmaker(bind=engine)


# para deixar o campo a nulo usar None

session= Session()



person = Person(0,"joao", "hotmail" )
#person.personal_tag=1
session.add(person)
session.commit()

#teste de funcao que adiciona uma pessoa
#adder()


person = Person(1,"miguel O VELHO", "gemail" )
person.personal_tag=1
#Muda data de validade
date=datetime(datetime.today().year,datetime.today().month, datetime.today().day,datetime.today().hour,datetime.today().minute,datetime.today().second)
person.created_date= date-timedelta(days=18000)

session.add(person)
session.commit()

person = Person(5,"miguel O SEGUNDO VELHO", "gemail900000" )
person.personal_tag=1
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

checkin = Checkin(1,2 , 3 , "blabla2", 7)
session.add(checkin)
session.commit()

#Funcao de update de um valor o synchronize_session pode ter o valor 'evaluate'
# session.query(Restaurant).filter(Restaurant.adress == "street").update({Restaurant.adress: "street2"}, synchronize_session=False)
# session.commit()


session.close()







                                                                    # testes das funcoes da lib

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
#teste do limpa expired data
limpa(Person)


#teste do alerta_vazio
alerta_vazio()


#teste do change validade
change_val(Person,146)





#teste do show validade
teste=show_val(Person)
print("\n\n\n\n TESTES show_val: %d"%(teste))


is_private(Person)
is_private(Restaurant)
is_private(Checkin)




#ve as tabelas que tao na BD   APAGAR
print("TABELAS NA BD\n\n\n\n\n")
print (engine.table_names())
print(Person.__name__)
print("TABELAS NA BD FIM\n\n\n\n\n")



                                                                            #parte responsavel pelo teste de query
Session = sessionmaker(bind=engine)
session= Session()


#teste para guardar set de privados
metas = session.query(Metatable).all()
for meta in metas:
    print ("\n\nTeste de metadados lista: %s proposito %s  categoria %s owner %s  origem  %s   validade %d  \n" %(meta.l_pessoal, meta.goal, meta.categorie, meta.data_owner, meta.data_source, meta.validade))



print("\n Persons data\n")
persons = session.query(Person).all()
for person in persons:
    print ("\n\nPessoa com o nome %s id %d e email %s    %s\n" %(person.name, person.id, person.email,person.created_date))

print("\n Restaurant data\n")
restaurants = session.query(Restaurant).all()
for restaurant in restaurants:
    print ("\n\nRestaurante com o nome %s id %d e a morada %s\n" %(restaurant.name, restaurant.id_r, restaurant.adress))


print("\nCheckin data\n")                                                                              #last query erro
checkins = session.query(Checkin).all()
for checkin in checkins:
    print ("\n\ncheckin com o id %d da pessoa com id %d no restaurante de id %d Descricao %s e Qualificacao %d \n" %(checkin.id_c , checkin.id , checkin.id_r, checkin.description, checkin.rating))

session.close()
