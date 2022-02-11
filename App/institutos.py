import mysql.connector
from config import config
from utils import *
from querys import *


def lista_instituto(cnx):
    sql = """ SELECT * FROM Instituto """
    data = None
    filtra_e_lista(cnx, data, sql)


def mostra_menu_instituto():
    print(80 * "#")
    print("""Menu
            Instituto                   ...
                1 - Lista Institutos    ...
                2 - Filtra Institutos   ...
                3 - Adiciona Instituto  ...
                                        ...
            
            v -  Voltar atrás 
            x - sair
        """)
    print(80 * "#")
    op = input("opção? ")
    print(80 * "#")
    return op


def main_instituto():
    cnx = mysql.connector.connect(**config)
    while True:
        op = mostra_menu_instituto()
        if op == '1':
            lista_instituto(cnx)
        elif op == "2":
            filtra_istitutos(cnx)
        elif op == "3":
            adiciona_instituto(cnx)
        elif op == "v":
            break
        elif op == "x":
            print("SAINDO.......")
            exit()

            # pass
            # #remove(cnx)

        else:
            print('Opcao nao permitida')
    pass


def adiciona_instituto(cnx):
    sql = """INSERT INTO instituto (
        designacao
        )
        VALUES (
        %(designacao)s)
        """
    atributo = input(f"designacao? ")
    data = {"designacao": atributo}

    with cnx.cursor() as cursor:
        cursor.execute(sql, data)
        cnx.commit()

    print("DADO ADICIONADO")
