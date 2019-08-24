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


for t in engine.table_names():
    print("TABELA - "+t)
    func(t)
