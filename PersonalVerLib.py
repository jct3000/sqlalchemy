from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, orm, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
# inclusao de classe geral de personal data
from sqlalchemy.ext.declarative import declared_attr


Base=declarative_base()
#nao necessario devido a funcao libInit
#engine = create_engine('sqlite:///user.db', echo=True)                         # ('sqlite:///:memory:', echo=True)   --- coloca a BD em memoria  se mudar para algo tipo user.db cria em file na dir

class PersonalData ( object ):

    @declared_attr
    def __tablename__ ( cls ):
        return cls . __name__ . lower ()
    #
    # __table_args__ = { 'mysql_engine' : 'InnoDB' }
    # __mapper_args__ = { 'always_refresh' : True }

    personal_tag=  Column ( Integer )
    created_date= Column(DateTime)
    #validade= Column ( Integer )



    def __init__(self, *args, **kwargs):
        #Inicializacoes
        self.personal_tag=1
        # introducao na lista da metatabela
        uniadder(self)
        #testes para tag da validade
        #self.validade=180                                                       #validade em dias 6 meses
        self.created_date=datetime.now().replace(microsecond=0)

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





#funcao de inicializacao que quando e chamada recebe
#o engine de forma a tanto a lib como a app estarem a usar o mesmo engine cria as classes e tabelas da lib
def libInit(engine_arg):
    global engine
    engine  = engine_arg
    Base.metadata.create_all(bind=engine)










                                            #Funcoes paralelas ao ORM



#Coloca apenas um valor na metatable para guardar os nomes de classes privadas
def uniadder(value):
    print("\n\n Uniadder: %s\n\n"%(value.__tablename__))
    Session = sessionmaker(bind=engine)
    session= Session()
    try:
        data = Metatable(value.__tablename__)
        session.add(data)
        session.commit()
    except:
        print("iniadder:Dados ja guardados")




#limpa dado uma classe privada todos os valores com prazo de validade espirado
def limpa(value):
    Session = sessionmaker(bind=engine)
    session= Session()
    for data in session.query(Metatable.validade).filter(Metatable.l_pessoal==value.__tablename__):
        prazo=data.validade
        print("\n\n\n\nlimpa: TESTE VALIDADE   %s\n\n\n"%(prazo))
    date=datetime.now().replace(microsecond=0)



        # Debbug das datas e etc apagar
        # for data in session.query(value).filter((value.created_date+timedelta(days=prazo))<=date):
        #     print("\n\n\n\n TESTE DATAS  %s\n\n\n"%(data.created_date))
        #     cenas=data.created_date+timedelta(days=prazo)
        #     print("\n\n\n\n TESTE DATAS2  %s\n\n\n"%(cenas))
        #     session.query(value).filter(cenas>date).delete()
        #     print("\n\n\n\n TESTE expressao  %r\n\n\n"%(cenas<date))

    session.query(value).filter((value.created_date)<date-timedelta(days=prazo)).delete()
    session.commit()




#Muda a validade na metatabela de uma determinada classe pessoal para o valor dado em dias
def change_val(class1, value):
    Session = sessionmaker(bind=engine)
    session= Session()
    session.query(Metatable).filter(Metatable.l_pessoal== class1.__tablename__).update({Metatable.validade: value}, synchronize_session=False)
    print("\n\n change_val: VAlidade modificada para %d\n\n\n"%(value))
    session.commit()







#print se a classe dada for privada erro: se a classe e publica nao diz nda
def is_private(class1):
    Session = sessionmaker(bind=engine)
    session= Session()
    for data in session.query(Metatable).filter(Metatable.l_pessoal==class1.__tablename__):
        print("\n\n\n\n is_private:CLASSE PRIVADA   \n\n\n")
    session.commit()








# avisa se algum valor da metatabela se encontra por preencher
def alerta_vazio():
    Session = sessionmaker(bind=engine)
    session= Session()
    for data in session.query(Metatable).filter(Metatable.goal == None):
        print("\n\n\nalerta_vazio Warning: goal of set %s is empty\n\n\n"%(data.l_pessoal))
    for data in session.query(Metatable).filter(Metatable.categorie == None):
        print("\n\n\nalerta_vazio Warning: categorie of set %s is empty\n\n\n"%(data.l_pessoal))
    for data in session.query(Metatable).filter(Metatable.data_owner == None):
        print("\n\n\nalerta_vazio Warning: data_owner of set %s is empty\n\n\n"%(data.l_pessoal))
    for data in session.query(Metatable).filter(Metatable.data_source == None):
        print("\n\n\nalerta_vazio Warning: data_source of set %s is empty\n\n\n"%(data.l_pessoal))
    for data in session.query(Metatable).filter(Metatable.validade == None):
        print("\n\n\nalerta_vazio Warning: validade of set %s is empty\n\n\n"%(data.l_pessoal))
        print("TESTE DE ALERTA")
    session.commit()

#teste de funcao para BD OUTDATED
# def adder():
#     Session = sessionmaker(bind=engine)
#     session= Session()
#     person = Person(2,"bruno", "hotmail2")
#     session.add(person)
#     session.commit()
#     #print("adder:Added one person\n")
