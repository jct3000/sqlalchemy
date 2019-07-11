from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, orm, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
# inclusao de classe geral de personal data
from sqlalchemy.ext.declarative import declared_attr

Base=declarative_base()
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




engine = create_engine('sqlite:///user.db', echo=True)                         # ('sqlite:///:memory:', echo=True)   --- coloca a BD em memoria  se mudar para algo tipo user.db cria em file na dir
Base.metadata.create_all(bind=engine)


                                            #Funcoes paralelas ao ORM



#Coloca apenas um valor na metatable para guardar os nomes de classes privadas
def uniadder(value):
    print(value)
    Session = sessionmaker(bind=engine)
    session= Session()
    try:
        data = Metatable(value)
        session.add(data)
        session.commit()
    except:
        print("Dados ja guardados")




#limpa dado uma classe privada todos os valores com prazo de validade espirado
def limpa(value):
    Session = sessionmaker(bind=engine)
    session= Session()
    for data in session.query(Metatable.validade).filter(Metatable.l_pessoal==value.__tablename__):
        prazo=data.validade
        print("\n\n\n\n TESTE VALIDADE   %s\n\n\n"%(data.validade))
    date=datetime(datetime.today().year,datetime.today().month, datetime.today().day,datetime.today().hour,datetime.today().minute,datetime.today().second)

    for data in session.query(value).filter((value.created_date+timedelta(days=prazo))<date):
        print("\n\n\n\n TESTE DATAS  %s\n\n\n"%(data.created_date))

    session.query(value).filter((value.created_date+timedelta(days=prazo))>date).delete()
    session.commit()

# avisa se algum valor da metatabela se encontra por preencher
def alerta_vazio():
    Session = sessionmaker(bind=engine)
    session= Session()
    for data in session.query(Metatable).filter(Metatable.goal == None):
        print("\n\n\nWarning: goal of set %s is empty\n\n\n"%(data.l_pessoal))
    for data in session.query(Metatable).filter(Metatable.categorie == None):
        print("\n\n\nWarning: categorie of set %s is empty\n\n\n"%(data.l_pessoal))
    for data in session.query(Metatable).filter(Metatable.data_owner == None):
        print("\n\n\nWarning: data_owner of set %s is empty\n\n\n"%(data.l_pessoal))
    for data in session.query(Metatable).filter(Metatable.data_source == None):
        print("\n\n\nWarning: data_source of set %s is empty\n\n\n"%(data.l_pessoal))
    for data in session.query(Metatable).filter(Metatable.validade == None):
        print("\n\n\nWarning: validade of set %s is empty\n\n\n"%(data.l_pessoal))
        print("TESTE DE ALERTA")
    session.commit()

#teste de funcao para BD
def adder():
    Session = sessionmaker(bind=engine)
    session= Session()
    person = Person(2,"bruno", "hotmail2")


    session.add(person)
    session.commit()
    #print("Added one person\n")
