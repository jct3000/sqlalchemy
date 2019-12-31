from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, orm, DateTime, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
# inclusao de classe geral de personal data
from sqlalchemy.ext.declarative import declared_attr

import sys

#inclusao para o checktables
from sqlalchemy.schema import Table
from sqlalchemy.schema import MetaData
meta = MetaData()
personalClasses={}

Base=declarative_base()
#nao necessario devido a funcao libInit
#engine = create_engine('sqlite:///user.db', echo=True)                         # ('sqlite:///:memory:', echo=True)   --- coloca a BD em memoria  se mudar para algo tipo user.db cria em file na dir


############################################################################################################################################################################################
# SUPERCLASSES METACLASSES E METATABELA
############################################################################################################################################################################################

#########################
#PersonalData
#
#superclass, de onde herdam as classes privadas
############################
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
        #testes para tag da validade
        #self.validade=180
        # introducao na lista da metatabela
        #uniadder(self)     outdated funtion
        Personal_tag_router(self)
                                                      #validade em dias 6 meses
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


#########################
#Metatable
#
#tabela onde sao guardados os valores transversais as classes segundo GRPD
############################
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

#########################
#Metaclass
#
#codigo chamado na creaccao do classe
############################



class CustomMetaClass(type(Base)):
    def __new__(meta, name, bases, dct):
        print '-----------------------------------'
        print "\n\nAllocating memory for class\n\n", name.lower()
        print meta
        print bases
        print dct
        #############################################################
        #add argument to class by metaprograming
        ############################################################
        # dct['xpto']= Column('xpto', String(),default='TESTE')
        # print '-----------------------------------'
        # print "\nNew dictionary in new\n"
        # print dct
        # print '-----------------------------------'

        if PersonalData in bases:
                personalClasses[name.lower()]=20

        #################################################################
        #AQUI E FEITO O GRAFO A PARTIR DE dct e a lista personalClasses
        #################################################################
        print '\n Vector Classes privadas'
        print (personalClasses)
        creategraph_lista(name.lower(),dct)
        aux_tag=Personal_tag_router_lista(name.lower(), grafo_lista, personalClasses)
        #debugg##########
        #print aux_tag
        #################
        bases, dct = Privitization(name, bases, aux_tag, personalClasses, dct)
        #introducao da inicializacao de personal data tags em todas as classes
        if PersonalData in bases:
            dct["__original_init__"]=dct["__init__"]
            dct["__init__"]=our_personnalInit
        print("bases after"+str(bases))
        print("\n\ndct after\n\n"+str(dct))

        return super(CustomMetaClass, meta).__new__(meta, name, bases, dct)

    def __init__(cls, name, bases, dct):
        print '-----------------------------------'
        print "\n\nInitializing class\n\n", name
        print cls
        print bases
        print dct
        #############################################################
        #add argument to class by metaprograming
        ############################################################
        # dct['foo']= Column('xpto', String())
        # print '-----------------------------------'
        # print "\nNew dictionary in init\n"
        # print dct
        # print '-----------------------------------'



        super(CustomMetaClass, cls).__init__(name, bases, dct)

############################################################################################################################################################################################
# FUNCOES DO FUNCIONAMENTO DA BIBLIOTECA
############################################################################################################################################################################################

#################################################################################################
#LIBINIT
#
#description:recebeo engine de forma a tanto a lib como a app estarem a usar
#o mesmo engine cria as classes e tabelas da lib USADO PK DOS ACESSOS directos A METATABELA
################################################################################################

def libInit(engine_arg):
    global engine
    engine  = engine_arg
    Base.metadata.create_all(bind=engine)


#################################################################################################
#UPDATE PERSONAL CLASSES
#
#description:recebe uma sessao e faz dump das classes na metatabela depois da sua criacao
################################################################################################

def updatePersonnalClasses(session):
    print "\n\nUpdating Metatable"
    print personalClasses
    for x in personalClasses.keys():
        try:                                                        #tentar retirar o try: e a parte do except
            data = Metatable(x)
            session.add(data)
            session.commit()
        except:
            print "Warnig updatePersonnalClasses: Already exists in Metatable"

############################################################################################################################################################################################
# FUNCOES DE METAPROGRAMACAO
############################################################################################################################################################################################


#################################################################################################
#PRIVITIZATION
#
#description:recebe nome, lista de classes pessoais bases e tag e coloca a a classe a extender da personal data se a tag for diferente de public
################################################################################################
def Privitization( name, bases, tag, personalClasses,dct):  #cls
    #Auto extend of a class to private
    if ((PersonalData not in bases) and (tag!="Public Class")):
        print '-----------------------------------'
        print"Inserting Personal Data Extend (Privitization)" + name
        bases=bases +(PersonalData, )
        print '-----------------------------------'
        print"Personal List"
        print (personalClasses)
        print"Inserting Personal List"
        personalClasses[name.lower()]=20
        print (personalClasses)
        print("bases after"+str(bases))
        print '-----------------------------------'
        # dct["__original_init__"]=dct["__init__"]
        # dct["__init__"]=our_personnalInit    #cls
    return bases ,dct


#################################################################################################
#OUR PERSONAL INIT
#
#description:funcao que modifica o construtor de classes privadas(excluindo roots) para correr o init da super classe PersonalData
################################################################################################
def our_personnalInit(self,  *kwargs):
    PersonalData.__init__(self)
    self.__original_init__(*kwargs)



############################################################################################################################################################################################

                                                                            #FUNCOES PARALELAS AO  ORM

############################################################################################################################################################################################


#################################################################################################
#UNIADDER (OUTDATED FUNC)
#
#description:Coloca APENAS UMA VEZ na metatable para guardar os nomes de classes privadas (outdated com introducao de metaclass)
################################################################################################

#
# def uniadder(value):
#     print("\n\n Uniadder: %s\n\n"%(value.__tablename__))
#     Session = sessionmaker(bind=engine)
#     session= Session()
#     try:
#         data = Metatable(value.__tablename__)
#         session.add(data)
#         session.commit()
#         session.close()
#     except:
#         print("iniadder:Dados ja guardados")


#################################################################################################
#LIMPA (MUDAR NOME)
#
#description:limpa dado uma classe privada todos os valores com prazo de validade espirado
################################################################################################


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
    session.close()

#################################################################################################
#CLEAN LIST
#
#description:retorna uma lista de todos os dados de uma classe que estao expired
################################################################################################

def clean_list(value):
    Session = sessionmaker(bind=engine)
    session= Session()
    for data in session.query(Metatable.validade).filter(Metatable.l_pessoal==value.__tablename__):
        prazo=data.validade
        print("\n\n\n\nclean_list: TESTE VALIDADE   %s\n\n\n"%(prazo))
    date=datetime.now().replace(microsecond=0)

    objects=session.query(value).filter((value.created_date)<date-timedelta(days=prazo)).all()
    results3={}
    results4={}
    n=0
    for object in objects:
        n=n+1
        for key, value  in object.__dict__.items():
            #print key, value
            results3.update( {str(key) : str(value)} )
        results3.pop('_sa_instance_state')
        results4[object.__tablename__+"_"+str(n)]=results3.copy()
        #results.append({'id':person.id,'name':person.name,'email':person.email, 'Personal_tag':person.personal_tag,'creation_date':person.created_date.isoformat()})  # data n funciona em jason
    session.commit()
    session.close()
    return results4
#################################################################################################
#CLEAN LIST OBJ
#
#description:retorna uma lista de todos os objectosclasse que estao expired
################################################################################################
def clean_list_obj(value):
    Session = sessionmaker(bind=engine)
    session= Session()
    for data in session.query(Metatable.validade).filter(Metatable.l_pessoal==value.__tablename__):
        prazo=data.validade
        print("\n\n\n\nclean_list: TESTE VALIDADE   %s\n\n\n"%(prazo))
    date=datetime.now().replace(microsecond=0)

    objects=session.query(value).filter((value.created_date)<date-timedelta(days=prazo)).all()
    list_obj=[]
    for object in objects:
        #print object
        list_obj.append(object)
        #results.append({'id':person.id,'name':person.name,'email':person.email, 'Personal_tag':person.personal_tag,'creation_date':person.created_date.isoformat()})  # data n funciona em jason
    session.commit()
    session.close()
    return list_obj



#################################################################################################
#CHANGE VAL
#
#description:Muda a validade na metatabela de uma determinada classe pessoal para o valor dado em dias
################################################################################################


def change_val(class1, value):
    Session = sessionmaker(bind=engine)
    session= Session()
    session.query(Metatable).filter(Metatable.l_pessoal== class1.__tablename__).update({Metatable.validade: value}, synchronize_session=False)
    print("\n\n change_val: Validade modificada para %d\n\n\n"%(value))
    session.commit()
    session.close()

#################################################################################################
#CHANGE GOAL
#
#description:Muda a objectivo dos dados na metatabela de uma determinada classe pessoal para a string dada
################################################################################################


def change_goal(class1, value):
    Session = sessionmaker(bind=engine)
    session= Session()
    session.query(Metatable).filter(Metatable.l_pessoal== class1.__tablename__).update({Metatable.goal: value}, synchronize_session=False)
    print("\n\n change_goal: Objectivo dos dados modificado para %s\n\n\n"%(value))
    session.commit()
    session.close()

#################################################################################################
#CHANGE CATEGORIE
#
#description:Muda a categoria na metatabela de uma determinada classe pessoal para a string dada
################################################################################################

def change_categorie(class1, value):
    Session = sessionmaker(bind=engine)
    session= Session()
    session.query(Metatable).filter(Metatable.l_pessoal== class1.__tablename__).update({Metatable.categorie: value}, synchronize_session=False)
    print("\n\n change_categorie: Categoria modificada para %s\n\n\n"%(value))
    session.commit()
    session.close()

#################################################################################################
#CHANGE DATA OWNER
#
#description:Muda a dono dos dados na metatabela de uma determinada classe pessoal para a string dada
################################################################################################

def change_data_owner(class1, value):
    Session = sessionmaker(bind=engine)
    session= Session()
    session.query(Metatable).filter(Metatable.l_pessoal== class1.__tablename__).update({Metatable.data_owner: value}, synchronize_session=False)
    print("\n\n data_owner: Dono dos dados modificado para %s\n\n\n"%(value))
    session.commit()
    session.close()

#################################################################################################
#CHANGE DATA SOURCE
#
#description:Muda a origem dos dados na metatabela de uma determinada classe pessoal para a string dada
################################################################################################

def change_data_source(class1, value):
    Session = sessionmaker(bind=engine)
    session= Session()
    session.query(Metatable).filter(Metatable.l_pessoal== class1.__tablename__).update({Metatable.data_source: value}, synchronize_session=False)
    print("\n\n _data_source: Origem dos dados modificado para %s\n\n\n"%(value))
    session.commit()
    session.close()





#################################################################################################
#SHOW VAL
#
#description:recebe uma classe devolve o valor da validade na metatabela
################################################################################################

def show_val(class1):
    Session = sessionmaker(bind=engine)
    session= Session()
    for data in session.query(Metatable.validade).filter(Metatable.l_pessoal==class1.__tablename__):
        prazo=data.validade
    return prazo

#################################################################################################
#SHOW GOAL
#
#description:recebe uma classe devolve o valor da goal na metatabela
################################################################################################

def show_goal(class1):
    Session = sessionmaker(bind=engine)
    session= Session()
    for data in session.query(Metatable.goal).filter(Metatable.l_pessoal==class1.__tablename__):
        goal=data.goal
    return goal

#################################################################################################
#SHOW CATEGORIE
#
#description:recebe uma classe devolve o valor da categoria na metatabela
################################################################################################

def show_categorie(class1):
    Session = sessionmaker(bind=engine)
    session= Session()
    for data in session.query(Metatable.categorie).filter(Metatable.l_pessoal==class1.__tablename__):
        categorie=data.categorie
    return categorie

#################################################################################################
#SHOW DATA OWNER
#
#description:recebe uma classe devolve o valor da dono dos dados na metatabela
################################################################################################

def show_data_owner(class1):
    Session = sessionmaker(bind=engine)
    session= Session()
    for data in session.query(Metatable.data_owner).filter(Metatable.l_pessoal==class1.__tablename__):
        data_owner=data.data_owner
    return data_owner
#################################################################################################
#SHOW DATA SOURCE
#
#description:recebe uma classe devolve o valor da origem dos dados na metatabela
################################################################################################

def show_data_source(class1):
    Session = sessionmaker(bind=engine)
    session= Session()
    for data in session.query(Metatable.data_source).filter(Metatable.l_pessoal==class1.__tablename__):
        data_source=data.data_source
    return data_source
#################################################################################################
#IS PRIVATE
#
#description: print se a classe dada for privada erro: se a classe e publica nao diz nda
################################################################################################

def is_private(class1):
    Session = sessionmaker(bind=engine)
    session= Session()
    data=session.query(Metatable).filter(Metatable.l_pessoal==class1.__tablename__).count()
    if data is 0:
        print("\n\n\n\n is_private:CLASSE PUBLICA   \n\n\n")
    else:
        print("\n\n\n\n is_private:CLASSE PRIVADA   \n\n\n")
    session.commit()
    session.close()





#################################################################################################
#ALERTA VAZIO (MUDAR NOME)
#
#description: avisa se algum valor da metatabela se encontra por preencher
################################################################################################

def alerta_vazio():
    Session = sessionmaker(bind=engine)
    session= Session()
    print("\n\nTESTE DE ALERTA\n\n")
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
    session.commit()
    session.close()




#################################################################################################
#SHOW PRIVATE DATA GIVEN CLASS AND ID
#
#description: recebe uma classe e um id e devolve os dados desse objecto e dos objectos das classes descendem diretamente
################################################################################################






def showclassdata( classe, id_aux, modulo="__main__"):
    print('\n\n\n---------------')
    print("showclassdata")
    Session = sessionmaker(bind=engine)
    session= Session()
    #1 saber a primary key da 1 classe
    id_pk=inspect(classe).primary_key[0].name
    results={}
    results2={}
    n=0
    ##debugg######
    # print id_pk
    # print type(id_pk)
    # print(sys.modules[modulo].__dict__["Person"])
    ##################
    #2guardar resultados da 1 pesquisa
    objects = session.query(classe).filter(classe.__dict__[id_pk]==id_aux)   #nao pode ser classe.id tem de ver a pk e e essa classe.id_pk mas isso n da
    for object in objects:
        for key, value  in object.__dict__.items():
            #print key, value
            results.update( {str(key) : str(value)} )
        results.pop('_sa_instance_state')
    print results
    results2[object.__tablename__+"_"+str(n)]=results.copy()
    results.clear()
    ####################
    #3guarda a chaves primarias e a classe correspondente
    keys={}
    keys[classe.__tablename__+"_"+str(n)]={id_pk : id_aux}

    #4 ve os descendentes e guarda
    descendentes=[]
    descendentes=ordered_find_direct_descend(grafo,classe.__tablename__)
    #5 apaga o pai
    if len(descendentes)>1:
        del descendentes[1]
    ##debugg#########
    # print('\n\n\n---------------')
    # print("primary keys")
    # print keys
    # print("descendentes")
    print descendentes
    # print descendentes[2]
    ################
    aux=[]
    aux2=[]
    aux.append(id_aux)
    for t in descendentes:
        n=0
        for x in aux:
            objects = session.query(sys.modules[modulo].__dict__[descendentes[t].capitalize()]).filter(sys.modules[modulo].__dict__[descendentes[t].capitalize()].__dict__[id_pk]==x)   #nao pode ser classe.id tem de ver a pk e e essa classe.id_pk mas isso n da
            new_id_pk=inspect(sys.modules[modulo].__dict__[descendentes[t].capitalize()]).primary_key[0].name
            for object in objects:
                keys[object.__tablename__+"_"+str(n)]={new_id_pk : object.__dict__[new_id_pk]}
                aux2.append(object.__dict__[new_id_pk])
                for key, value  in object.__dict__.items():
                    #print key, value
                    results.update( {str(key) : str(value)} )
                results.pop('_sa_instance_state')
                results2[object.__tablename__+"_"+str(n)]=results.copy()
                results.clear()
                n=n+1
        aux=[]
        aux=aux2
        aux2=[]
        id_pk=new_id_pk
        print results

    ##debugg#########
    # print descendentes[t].capitalize()
    ###############
        ##debbug#####
    # print type(sys.modules[modulo].__dict__[descendentes[t].capitalize()])
    # print id_pk
    # print keys["person_0"]
    # print keys
    # print "\nDescarga resultados"
    for t in results2:
        print t
        print results2[t]
    # print "\nResultado especifico"
    # print results2["grade_1"]
        ############
    ####################

    # aux=[]
    #
    # relationship_list = [str(list(column.remote_side)[0]).split('.')[0] for column in inspect(classe).relationships]
    # aux.extend(relationship_list)
    # results.update( {'Relations' : aux} )
    # ##debbugg########
    # print('\n\n\n---------------')
    # print("c /relacoes")
    # ###############################
    # results.update( {'Descendentes' : ordered_find_direct_descend(grafo,classe.__tablename__)} )
    # print results
    # ###################

    session.close()
    return results2





#################################################################################################
#SHOW PRIVATE OBJ DATA GIVEN CLASS AND ID
#
#description: recebe uma classe e um id e devolve os dados desse objecto e dos objectos das classes descendem diretamente (lista de objectos)
#obj_list- tem os objectos separados, obj_list2, tem so a lista de objectos
################################################################################################






def showclassdata_obj( classe, id_aux, modulo="__main__"):
    print('\n\n\n---------------')
    print("showclassdata_OBJ")
    Session = sessionmaker(bind=engine)
    session= Session()
    #1 saber a primary key da 1 classe
    id_pk=inspect(classe).primary_key[0].name
    results={}
    obj_list=[]
    obj_list2=[]
    n=0
    ##debugg######
    # print id_pk
    # print type(id_pk)
    # print(sys.modules[modulo].__dict__["Person"])
    ##################
    #2guardar resultados da 1 pesquisa
    objects = session.query(classe).filter(classe.__dict__[id_pk]==id_aux)   #nao pode ser classe.id tem de ver a pk e e essa classe.id_pk mas isso n da
    for object in objects:
        obj_list.append(object)
        obj_list2.append(object)
    print obj_list
    results[object.__tablename__+"_"+str(n)]=obj_list
    obj_list=[]
    ####################
    #3guarda a chaves primarias e a classe correspondente
    keys={}
    keys[classe.__tablename__+"_"+str(n)]={id_pk : id_aux}

    #4 ve os descendentes e guarda
    descendentes=[]
    descendentes=ordered_find_direct_descend(grafo,classe.__tablename__)
    #5 apaga o pai
    if len(descendentes)>1:
        del descendentes[1]
    aux=[]
    aux2=[]
    aux.append(id_aux)
    for t in descendentes:
        n=0
        for x in aux:
            objects = session.query(sys.modules[modulo].__dict__[descendentes[t].capitalize()]).filter(sys.modules[modulo].__dict__[descendentes[t].capitalize()].__dict__[id_pk]==x)   #nao pode ser classe.id tem de ver a pk e e essa classe.id_pk mas isso n da
            new_id_pk=inspect(sys.modules[modulo].__dict__[descendentes[t].capitalize()]).primary_key[0].name
            for object in objects:
                keys[object.__tablename__+"_"+str(n)]={new_id_pk : object.__dict__[new_id_pk]}
                aux2.append(object.__dict__[new_id_pk])
                obj_list.append(object)
                obj_list2.append(object)
            results[object.__tablename__+"_"+str(n)]=obj_list
            obj_list=[]
            n=n+1
        aux=[]
        aux=aux2
        aux2=[]
        id_pk=new_id_pk
        print results
        print("\ntest obj list\n")
        print obj_list2
    session.close()
    return results











############################################################################################################################################################################################
#FUNCAO DE CREACAO E ESTUDO DE GRAFOS
############################################################################################################################################################################################


################################################################################
#creategraph_lista
#Desciption:Nova funcao de criacao de grafos sem metatabela usando a lista de classes pessoais
################################################################################
grafo_lista={}
def creategraph_lista(name,dct,):
    print("------------------")
    print '\nLISTA\n'
    aux=str(dct.values())
    print aux
    print("------------------")
    index= 0
    fathers=[]
    while index < len(aux):
        index = aux.find('ForeignKey(', index)
        if index == -1:
            break
        #debbug apagar########
        print('FK found at', index)
        ########################
        index += 12
        fathers.append((aux[index:]).split('.',1)[0])
    print("\n fathers of " +name)
    print fathers
    grafo_lista[name]=fathers
    print("\n Grafo da lista")
    print grafo_lista



################################################################################
#PERSONAL TAG ROUTER LISTA
#
#Desciption:recebe uma nome, grafo, e lista de classes pessoais e introduz na sua personal tag a root ou roots mais proxima
################################################################################



def Personal_tag_router_lista(name, grafo_lista, personalClasses):
    print("\n\nTAG LISTA\n\n")
    n=0
    value="Public Class"
    #debugg##########
    #print "NOME:"+name
    #####################
    for x in personalClasses.keys():
        #debugg##########
        #print x
        #################
        if(find_shortest_path(grafo_lista,name, x) is None):
            pass
        elif(((len(find_shortest_path(grafo_lista, name,x))==1))and(n==0)):
            value=name
        elif ((n<=len(find_shortest_path(grafo_lista, name, x)))and (len(find_shortest_path(grafo_lista,name,x))>1)):
            if(n==len(find_shortest_path(grafo_lista, name, x))):
                n=len(find_shortest_path(grafo_lista, name,x))
                value=value + ',' + x
            else:
                n=len(find_shortest_path(grafo_lista, name,x))
                value=x
    print ("\nPERSONAL TAG\n")
    print value
    return value



###############################################################################

################################################################################
#CREATE GRAPH
#
#Desciption:recebe uma class e com as FK dessa class cria um no de grafo
################################################################################

def creategraph(t):
    table = Table(t, meta, autoload=True, autoload_with=engine)
    #debugg##########
    print("------------------")
    print("Entrou na funcao com "+str(table))
    print("------------------")
    ###############
    neighbors=[]
    for fkey in table.foreign_keys:
        fkey=str(fkey).split(".")[0]
        aux=(fkey[13:])
        #debugg##########
        print("foreign key "+aux)
        #########################
        neighbors.append(aux)
    #debugg##########
    print("\n\n-----neighbours-----")
    print(neighbors)
    ################
    grafo[str(table)]=neighbors


################################################################################
#FIND PATH
#
#Desciption:recebe uma grafo, um no de start e um de end e devolve um caminho
################################################################################

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


################################################################################
#FIND ALL PATH
#
#Desciption:recebe uma grafo, um no de start e um de end e devolve todos os caminhos
################################################################################


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

################################################################################
#FIND SHORTEST PATH
#
#Desciption:recebe uma grafo, um no de start e um de end e devolve o menor caminho
################################################################################
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



################################################################################
#PERSONAL TAG ROUTER
#
#Desciption:recebe uma classe e introduz na sua personal tag a root ou roots mais proxima
################################################################################
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
        elif ((n<=len(find_shortest_path(grafo, classe.__tablename__, x.l_pessoal)))and (len(find_shortest_path(grafo, classe.__tablename__,x.l_pessoal))>1)):
            if(n==len(find_shortest_path(grafo, classe.__tablename__, x.l_pessoal))):
                n=len(find_shortest_path(grafo, classe.__tablename__,x.l_pessoal))
                value=value + ',' + x.l_pessoal
            else:
                n=len(find_shortest_path(grafo, classe.__tablename__,x.l_pessoal))
                value=x.l_pessoal

    classe.personal_tag=value
    #session.query(Classe).filter(Classe.id == Classe.id).update({Classe.personal_tag: value}, synchronize_session=False)
    session.commit()
    session.close()





###############################################################################
#FUNCAO DE DESCENDENTES DIRETOS
#
#Desciption: recebe um grafo e um nome classe e devolve o caminho pelos descendentes directos ate a folha da arvore
###############################################################################


# def find_direct_descend(graph, father, path=[]):     #OUTDATED (ordered e melhor)
#     n=0
#     Session = sessionmaker(bind=engine)
#     session= Session()
#     if(session.query(Metatable).filter_by(l_pessoal=father).scalar() is None):
#         return 'Public Class'
#     data= session.query(Metatable).all()
#     for t in data:
#         if((find_shortest_path(graph,t.l_pessoal,father)) is None or n<len(find_shortest_path(graph,t.l_pessoal,father))==1):
#             path=path
#         elif(n<len(find_shortest_path(graph,t.l_pessoal,father))):
#             n=len(find_shortest_path(graph,t.l_pessoal,father))
#             path=(find_shortest_path(graph,t.l_pessoal,father))
#     session.commit()
#     session.close()
#     return path


def ordered_find_direct_descend(graph, father, path=[]):
    n=0
    Session = sessionmaker(bind=engine)
    session= Session()
    if(session.query(Metatable).filter_by(l_pessoal=father).scalar() is None):
        return 'Public Class'
    data= session.query(Metatable).all()
    for t in data:
        if((find_shortest_path(graph,t.l_pessoal,father)) is None or n<len(find_shortest_path(graph,t.l_pessoal,father))==1):
            path=path
        elif(n<len(find_shortest_path(graph,t.l_pessoal,father))):
            n=len(find_shortest_path(graph,t.l_pessoal,father))
            path=(find_shortest_path(graph,t.l_pessoal,father))
    path2={}
    for t in path:
        path2[len(find_shortest_path(graph,t,father))]=t

    session.commit()
    session.close()
    return path2

###############################################################################
