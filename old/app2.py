from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# inclusao de classe geral de personal data
from sqlalchemy.ext.declarative import declared_attr




Base=declarative_base()


class PersonalData (Base):

    @declared_attr
    def __tablename__ ( cls ):
        return cls . __name__ . lower ()
    #
    # __table_args__ = { 'mysql_engine' : 'InnoDB' }
    # __mapper_args__ = { 'always_refresh' : True }

    personal_tag=  Column ( Integer, primary_key=True )                         #necessita sempre de primary key para sair da base

    def __init__(self, *args, **kwargs):
        print("Personal_Data\n\n")
        Base.__init__(self, *args, **kwargs)








class Person (Base):
    __tablename__ = 'person'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    email = Column ('email', String, unique=True)
    chekin_p=relationship("Checkin")

    def __repr__(self):
        return "<Person(name='%s', email='%s')>" % (self.name, self.email)

    def __init__(self, id, name, email):
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


Session = sessionmaker(bind=engine)                                             #Parte responsavel pelos commits dos objectos para a DB


session= Session()
person = Person(0,"joao", "hotmail" )

#person.personal_tag=1




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


session.close()


#                                                                             #parte responsavel pelo teste de query
#
# session= Session()
# persons = session.query(Person).all()
# for person in persons:
#     print ("\nPessoa com o nome %s id %d e email %s\n" %(person.name, person.id, person.email))
#
# restaurants = session.query(Restaurant).all()
# for restaurant in restaurants:
#     print ("\nRestaurante com o nome %s id %d e a morada %s\n" %(restaurant.name, restaurant.id_r, restaurant.adress))
#
#                                                                               #last query erro
# checkins = session.query(Checkin).all()
# for checkin in checkins:
#     print ("\ncheckin com o id %d da pessoa com id %d no restaurante de id %d Descricao %s e Qualificacao %d \n" %(checkin.id_c , checkin.id , checkin.id_r, checkin.description, checkin.rating))
#
# session.close()
