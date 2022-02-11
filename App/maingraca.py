# pip install mysql-connector-python

import mysql.connector
from config import config
from App.querys import *
from institutos import *
from esaçoalimentar import *
from cliente import *
from fornecedores import *
import traceback


def mostra_menu_le_opcao():
    print(80 * "#")
    print("""Menu                 
                1 - Institutos         ...
                2 - Espaço Alimentar   ...
                3 - Clientes           ...
                4 - Fornecedores       
                ...
                
            v -  Voltar atrás 
            x - sair
        """)
    print(80 * "#")
    op = input("opção? ")
    print(80 * "#")
    return op


def main():
    # try:
    cnx = mysql.connector.connect(**config)
    while True:
        try:
            op = mostra_menu_le_opcao()
            if op == "1":
                main_instituto()
            elif op == "2":
                esapço_alimentaruni(cnx)
            elif op == "3":
                mcliente()
            elif op == "4":
               main_fornecedores(cnx)
            elif op == "v":
                break





        except mysql.connector.Error as err:
            print('Ups! Ocorreu um erro!')
            print(err.errno)
            traceback.print_exc()
        else:
            cnx.close()


# def  lista_instituto(cnx):
#     op=()
#     while True:
#         if op ==1:
#             AliESEC()
#         # elif op==2:
#         #     AliISE()
#         # elif op == 3:
#         #     AliESGHT()
#         # elif op == 4:
#         #     AliEC()
#         # elif op ==5:
#         #     Cantina()
#         elif op == "X":
#             break


# if __name__ == "__main__":


