from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, orm, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
# inclusao de classe geral de personal data
from sqlalchemy.ext.declarative import declared_attr


from mymodel import *

engine = create_engine('sqlite:///user.db', echo=True)                         # ('sqlite:///:memory:', echo=True)   --- coloca a BD em memoria  se mudar para algo tipo user.db cria em file na dir
Base.metadata.create_all(bind=engine)



class PersonalData ( object ):

    @declared_attr
    def __tablename__ ( cls ):
        return cls . __name__ . lower ()
    #
    # __table_args__ = { 'mysql_engine' : 'InnoDB' }
    # __mapper_args__ = { 'always_refresh' : True }

    personal_tag=  Column ( Integer )
    created_date= Column(DateTime)
    #meter na metatabela
    lista=set()
    validade= Column ( Integer )



    def __init__(self, *args, **kwargs):
        self.personal_tag=1
        print("\nPersonal_Data\n")
        PersonalData.lista.add(self.__tablename__)
        print("\n lista de classes privadas\n")
        uniadder(self.__tablename__)
        print(self.lista)
        print("\n")                                                             #Inicializacoes



        self.validade=180                                                       #validade em dias 6 meses
        self.created_date=datetime(datetime.today().year,datetime.today().month, datetime.today().day,datetime.today().hour,datetime.today().minute,datetime.today().second)
        print("\n DATA\n")
        print(self.created_date)
        print(self.created_date+timedelta(days=self.validade))
        print("\n FIM\n")



        #Base.__init__(self, *args, **kwargs)

    @orm.reconstructor
    def init_on_load(self):                                                     #printa sempre que for buscar algo a BD
        print("\n\nCarregado da DB\n\n")

    # def __getattribute__(self, name):                                         #printa todos os getters
    #     print ("getting attribute %s" %name)
    #     return object.__getattribute__(self, name)
    #
    # def __setattr__(self, name, val):                                         #printa todos os getters
    #     print ("   setting attribute %s to %r" %(name, val))
    #     return object.__setattr__(self, name, val)








Base=declarative_base()


class Metatable (Base):
    __tablename__ = 'metatable'
    id_sec= Column('id_sec', Integer, primary_key=True, unique=True)
    l_pessoal= Column('pessoal', String, unique=True )
    goal= Column('goal', String, nullable=True )
    data_owner= Column('data_owner', String)
    categorie= Column('categorie', String)
    data_source = Column('data_source', String)
    validade=Column('validade', Integer)


    def __init__(self, value):
        self.l_pessoal= value
        self.goal="statistic"
        self.categorie="External"
        self.data_owner="DONO"
        self.data_source="client"
        self.validade=180








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



# engine = create_engine('sqlite:///user.db', echo=True)                         # ('sqlite:///:memory:', echo=True)   --- coloca a BD em memoria  se mudar para algo tipo user.db cria em file na dir
# Base.metadata.create_all(bind=engine)


Session = sessionmaker(bind=engine)                                             #Parte responsavel pelos commits dos objectos para a DB





# para deixar o campo a nulo usar None




session= Session()
person = Person(0,"joao", "hotmail" )
#person.personal_tag=1
session.add(person)
session.commit()

#teste de funcao que adiciona uma pessoa
adder()


person = Person(1,"miguel", "gemail" )
person.personal_tag=1
#Muda data de validade
date=datetime(datetime.today().year,datetime.today().month, datetime.today().day,datetime.today().hour,datetime.today().minute,datetime.today().second)
person.created_date= date-timedelta(days=18000)

session.add(person)
session.commit()






# session.query(Person).filter(Person.id==0).delete()                           # Para apagar um objecto com querie
# session.commit()                                                              # Para apagar um objecto com querie




restaurant = Restaurant(1,"Dinner","street" )
session.add(restaurant)
session.commit()




checkin = Checkin(0,1 , 0 , "blabla", 3)
session.add(checkin)
session.commit()


#Funcao de update de um valor o synchronize_session pode ter o valor 'evaluate'
# session.query(Restaurant).filter(Restaurant.adress == "street").update({Restaurant.adress: "street2"}, synchronize_session=False)
# session.commit()


session.close()




limpa(Person)



alerta_vazio()

change_val(Person,146)

is_private(Person)
is_private(Restaurant)
is_private(Checkin)
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
