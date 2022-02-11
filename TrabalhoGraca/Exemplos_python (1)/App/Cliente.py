import mysql.connector
from config import config
from utils import *
from querys import *

def lista_clientes(cnx):
    sql= """SELECT * FROM cliente"""
    data= None
    filtra_e_lista(cnx,data,sql)



def menu_clientes(cnx):
    print(80*"#")
    print("""MENU
             Clinetes
             1- lista Clinetes
             2- Filtra clientes
             3- Adiciona cliente
             
             
             X- Sair 
             """)
    print(80*"#")
    op=input("opção:")
    print(80*"#")
    return op


def adiciona_cliente(cnx):
    sql = """INSERT INTO cliente(
        nome, apelido, numero_telefone 
        )
        Values(
        %(nome)s
        %(apelido)s
        %numero_telfone)s
        %(cod_cliente)s)"""
    atributo = input(f"nome")
    data = {"nome": atributo}

    with cnx.cursor() as cursor:
        cursor.execute(sql, data)
        cnx.commit()

    print("DADO ADICIONADO")


def cliente():
    cnx = mysql.connector.connect(**config)
    while True:
        op=menu_clientes(cnx)
        if op== "1":
            lista_clientes(cnx)
        elif op== "2":
            filtra_cliente(cnx)
        elif op== "3":
            adiciona_cliente(cnx)
        elif op== "X":
            print("SAINDO....")
            exit()

        else:
            print("Opção iválida")
    pass


