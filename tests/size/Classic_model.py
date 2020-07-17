from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
import sys
Base=declarative_base()

class Person (Base):
    __tablename__ = 'person'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    email = Column ('email', String, unique=True)
    checkin_p=relationship("Checkin")


    def __init__(self, id, name, email):
        self.id=id
        self.name=name
        self.email=email


    class Restaurant (Base):
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


class Checkin(Base):
      __tablename__ = 'checkin'

      id_c=Column('id_c', Integer, primary_key=True)
      id=Column(Integer, ForeignKey('person.id'))
      id_r= Column(Integer, ForeignKey('restaurant.id_r'))
      description = Column('description', String)
      rating = Column ('rating', Integer)


      def __init__(self, id_c, id, id_r, description, rating):
  #        PersonalData.__init__(self)
          self.id_c=id_c
          self.id=id
          self.id_r=id_r
          self.description=description
          self.rating=rating



engine = create_engine('sqlite:///user.db', echo=True)                         # ('sqlite:///:memory:', echo=True)   --- coloca a BD em memoria  se mudar para algo tipo user.db cria em file na dir
Base.metadata.create_all(bind=engine)


Session = sessionmaker(bind=engine)




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







Session = sessionmaker(bind=engine)
session= Session()

print("\n Persons data\n")
persons = session.query(Person).all()
for person in persons:
    print ("\n\nPessoa com o nome %s id %d e email %s \n" %( person.name, person.id, person.email))
session.close()


print('\nDuration: {}'.format(end_time - start_time))
