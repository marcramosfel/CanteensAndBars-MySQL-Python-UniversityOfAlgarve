import mysql.connector
from config import config
from utils import *
from querys import *


def lista_espaço(cnx):
    sql="""SELECT * FROM espacoalimentar"""
    data= None
    filtra_e_lista(cnx,data,sql)

def esapço_alimentaruni(cnx):
    cnx=mysql.connector.connect(**config)
    while True:
        op=mostra_menu_espaco(cnx)
        if  op== "1":
            lista_espaço(cnx)

        elif op== "2":
            filtra_espaco(cnx)

        elif op== "3":
            adiciona_espaco(cnx)
        elif op == "v":
            break


        elif op== "X":
            print("Saindo.....")
            exit()



        else:
            print("Opção inválida")
    pass



def mostra_menu_espaco(cnx):
    print(80 * "#")
    print("""MENU 
    ESPAÇO ALIMENTAR
              1- Lista espaço alimentar
              2- Filtra espaço
              3- Adiciona espaço
              
              v -  Voltar atrás 
              X-Sair """)
    print(80*"#")
    op=input("opção:")
    print(80*"#")
    return op


def adiciona_espaco(cnx):
    sql="""INSERT INTO espacoalimentar(
    designacao
    )
    Values(
    %(nome)s
    %(idinstituto)s)"""
    atributo= input(f"nome")
    data= {"nome":atributo}

    with cnx.cursor() as cursor:
        cursor.execute(sql,data)
        cnx.commit()

    print("DADO ADICIONADO")
