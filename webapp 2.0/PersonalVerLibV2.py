from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, orm, DateTime, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
# inclusao de classe geral de personal data
from sqlalchemy.ext.declarative import declared_attr


#inclusao para o checktables
from sqlalchemy.schema import Table
from sqlalchemy.schema import MetaData
meta = MetaData()

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

    personal_tag=  Column (String)
    created_date= Column(DateTime)
    #validade= Column ( Integer )



    def __init__(self, *args, **kwargs):
        #Inicializacoes
        #self.personal_tag=1
        # introducao na lista da metatabela
        uniadder(self)
        Personal_tag_router(self)
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



# retorna uma lista de todos os dados de uma classe que estao expired
def clean_list(value):
    Session = sessionmaker(bind=engine)
    session= Session()
    for data in session.query(Metatable.validade).filter(Metatable.l_pessoal==value.__tablename__):
        prazo=data.validade
        print("\n\n\n\nclean_list: TESTE VALIDADE   %s\n\n\n"%(prazo))
    date=datetime.now().replace(microsecond=0)

    persons=session.query(value).filter((value.created_date)<date-timedelta(days=prazo)).all()
    results=[]
    for person in persons:
        results.append({'id':person.id,'name':person.name,'email':person.email, 'Personal_tag':person.personal_tag,'creation_date':person.created_date.isoformat()})  # data n funciona em jason
    #session.close()
    session.commit()
    return results

#Muda a validade na metatabela de uma determinada classe pessoal para o valor dado em dias
def change_val(class1, value):
    Session = sessionmaker(bind=engine)
    session= Session()
    session.query(Metatable).filter(Metatable.l_pessoal== class1.__tablename__).update({Metatable.validade: value}, synchronize_session=False)
    print("\n\n change_val: VAlidade modificada para %d\n\n\n"%(value))
    session.commit()


#devolde o prazo de validade de uma classe dada
def show_val(value):
    Session = sessionmaker(bind=engine)
    session= Session()
    for data in session.query(Metatable.validade).filter(Metatable.l_pessoal==value.__tablename__):
        prazo=data.validade
    return prazo


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




#################################################################################################
#SHOW PRIVATE DATA GIVEN CLASS AND ID
################################################################################################


#ERROR: append with no idea of what the classe is coded no idea that as a classe.name

def showclassdata(classe, id_aux):
    Session = sessionmaker(bind=engine)
    session= Session()
    objects = session.query(classe).filter(classe.id==id_aux)
    #results=[]
    results={}
    aux=[]

    for object in objects:
        for key, value  in object.__dict__.items():
            #print key, value
            results.update( {str(key) : str(value)} )
        results.pop('_sa_instance_state')
        #results.append(str(object.__dict__.items()))# maneira melhor se tirar o str posso fazer pop mas deixa de ser string e o data time passa se com o jason
        #results.append("["+str(object.__dict__.items()).split(",",2)[2])# maneira melhor se tirar o str posso fazer pop mas deixa de ser string e o data time passa se com o jason



    relationship_list = [str(list(column.remote_side)[0]).split('.')[0] for column in inspect(classe).relationships]
    aux.extend(relationship_list)
    results.update( {'Relations' : aux} )
    for relationship in relationship_list:
        print("\n\n\n\n\n\n\n HERE \n\n\n\n\n\n")
        #print(sys.modules[__name__])
        #eval("webapp import *")
        #print(type(eval(relationship.capitalize()))) # para saber o tipo aqui eval(relationship.capitalize())
        #objects = session.query(relationship.capitalize()).filter(relationship.capitalize().id==id_aux)   #relatioship continua a ser string
        #for object in objects:
            #agrupar os resultados como em append anterior
            #results.append(str(object.__dict__.items()))# maneira melhor se tirar o str posso fazer pop mas deixa de ser string e o data time passa se com o jason
    session.close()
    return results

################################################################################
#FUNCAO DE CREACAO E ESTUDO DE GRAFOS
################################################################################


def creategraph(t):
    table = Table(t, meta, autoload=True, autoload_with=engine)
    print("------------------")
    print("Entrou na funcao com "+str(table))
    print("------------------")
    neighbors=[]
    for fkey in table.foreign_keys:
        fkey=str(fkey).split(".")[0]
        aux=(fkey[13:])
        print("foreign key "+aux)
        neighbors.append(aux)
    print("\n\n-----neighbours-----")
    print(neighbors)
    grafo[str(table)]=neighbors




def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath: return newpath
    return None

def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start):
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

grafo={}


def Personal_tag_router(classe):
    n=0
    value="default"
    #Preocupacao com utilizacao de None assim
    for t in engine.table_names():
        creategraph(t)


    #Metatable usage
    Session = sessionmaker(bind=engine)
    session= Session()
    data= session.query(Metatable).all()
    for x in data:
    #for t in engine.table_names():
    #None part is useless TIRAR
        if(find_shortest_path(grafo, classe.__tablename__, x.l_pessoal) is None):
            pass
        elif(((len(find_shortest_path(grafo, classe.__tablename__,x.l_pessoal))==1))and(n==0)):      #tinha um if((find_shortest_path(grafo, classe.__tablename__, x.l_pessoal) is None) or(len(find_shortest_path(grafo, classe.__tablename__,x.l_pessoal))==1))and(n==0)):
            value=classe.__tablename__
        elif ((n<len(find_shortest_path(grafo, classe.__tablename__, x.l_pessoal)))and (len(find_shortest_path(grafo, classe.__tablename__,x.l_pessoal))>1)):
            n=len(find_shortest_path(grafo, classe.__tablename__,x.l_pessoal))
            value=x.l_pessoal

    classe.personal_tag=value
    #session.query(Classe).filter(Classe.id == Classe.id).update({Classe.personal_tag: value}, synchronize_session=False)
    session.commit()
    session.close()





###############################################################################
#FUNCAO DE DESCENDENTES DIRETOS
###############################################################################

def find_direct_descend(graph, father, path=[]):
    n=0
    Session = sessionmaker(bind=engine)
    session= Session()
    if(session.query(Metatable).filter_by(l_pessoal=father).scalar() is None):
        return 'Public'
    data= session.query(Metatable).all()
    for t in data:
        if((find_shortest_path(graph,t.l_pessoal,father)) is None or n<len(find_shortest_path(graph,t.l_pessoal,father))==1):
            path=path
        elif(n<len(find_shortest_path(graph,t.l_pessoal,father))):
            n=len(find_shortest_path(graph,t.l_pessoal,father))
            path=(find_shortest_path(graph,t.l_pessoal,father))
    session.commit()
    session.close()
    return path


###############################################################################
