import mysql.connector
from config import config
from utils import *
from querys import *


def menu_fornecedores():
    print(80 * "#")
    print("""MENU
    Fornecedores
            1- Lista de fornecedores
            2- Filtra fornecedores
            3- adiciona fornecedor
            
            
            
            x- sair
            """)
    print(80 * "#")
    op=input("opção")
    print(80 * "#")
    return op



def lista_fornecedores(cnx):
    sql="""SELECT * FROM fornecedor"""
    data= None
    filtra_e_lista(cnx,data,sql)


def main_fornecedores(cnx):
    cnx = mysql.connector.connect(**config)
    while True:
        op=menu_fornecedores()
        if op== "1":
            lista_fornecedores(cnx)
        elif op== "2":
            filtra_fornecedor(cnx)
        elif op== "3":
            adiciona_fornecedor(cnx)
        elif op== "X":
            print("Saindo....")
            exit()
        else:
            print("Opção inválida")
    pass


def adiciona_fornecedor(cnx):
    sql="""INSERT INTO fornecedor (
    nome)
    VALUES (
    %(nome)s)"""
    atributo=input(f"nome?")
    data={"nome": atributo}

    with cnx.cursor() as cursor:
        cursor.execute(sql, data)
        cnx.commit()

    print("DADO ADICIONADO")



