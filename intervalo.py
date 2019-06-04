from sqlalchemy import Column, Integer, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, aliased
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

# inclusao de classe geral de personal data
from sqlalchemy.ext.declarative import declared_attr


Base = declarative_base()

class PersonalData ( object ):

    @declared_attr
    def __tablename__ ( cls ):
        return cls . __name__ . lower ()
    #
    # __table_args__ = { 'mysql_engine' : 'InnoDB' }
    # __mapper_args__ = { 'always_refresh' : True }

    personal_tag=  Column ( Integer )

    @hybrid_property                                                        #prova a introducao de um metodo a partir de uma classe base
    def length(self):
        return self.end - self.start

    def __init__(self):
        print("Classe privada gerada\n\n")
        self.personal_tag=1




class Interval(PersonalData, Base):
    __tablename__ = 'interval'

    id = Column(Integer, primary_key=True)
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)

    def __init__(self, start, end):
        PersonalData.__init__(self)
        self.start = start
        self.end = end
                                         #Flag de classe gerada

    # @orm.reconstructor                                                    #supostamente correr este codigo a seguir a cada new
    # def init_on_load(self):
    #     print("Classe privada gerada\n\n")


    @hybrid_method
    def contains(self, point):
        return (self.start <= point) & (point <= self.end)

    @hybrid_method
    def intersects(self, other):
        return self.contains(other.start) | self.contains(other.end)



i1 = Interval(5, 10)
i2=Interval(9, 20)
i3=Interval(3, 5)
A=i1.length
B=i1.intersects (i2)
C=i2.intersects (i3)
print A
print B
print C
