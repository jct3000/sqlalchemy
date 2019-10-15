from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, orm, DateTime, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
from sqlalchemy.schema import Table
from sqlalchemy.schema import MetaData

# inclusao de classe geral de personal data
from sqlalchemy.ext.declarative import declared_attr


engine = create_engine('sqlite:///user.db', echo=False)                         # ('sqlite:///:memory:', echo=True)   --- coloca a BD em memoria  se mudar para algo tipo user.db cria em file na dir

meta = MetaData()







#ve as tabelas que tao na BD   APAGAR
print("\n\n\n\nTABELAS NA BD\n")
print (engine.table_names())
print("\n\n\n\nFIM TABELAS NA BD\n")



def func(t):
    person_table = Table(t, meta, autoload=True, autoload_with=engine)
    print("------------------")
    print(person_table)
    for fkey in person_table.foreign_keys:
        #chama func de grafo         func(aux)
        print(fkey)
        fkey=str(fkey).split(".")[0]
        aux=(fkey[13:])
        print(aux.capitalize())





################################################################################
#FUNCAO DE CREACAO DE GRAFOS
################################################################################

grafo={}
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


for t in engine.table_names():
    #print("TABELA - "+t)
    #func(t)
    creategraph(t)
print("\n\n--------Grafo---------")
print (grafo)
print("\n\n--------TODOS CAMINHOS---------")
print(find_all_paths(grafo, 'grade', 'restaurant'))
print("\n\n--------CAMINHO MAIS PEQUENO---------")
print(find_shortest_path(grafo, 'grade', 'restaurant'))
print("\n\n-------- UM CAMINHO---------")
print(find_path(grafo, 'checkin', 'person'))


################################################################################
#TESTES
###############################################################################
# levels=0
# etc="alo"
# results={}
# results[levels]=etc
# for x, y in results.items():
#     print(x,y)
