import mysql.connector
from estatisticas import *
from fatura import *
from funcionarios import *


def mostra_menu_le_opcao():
    print(80 * "#")
    print("""Menu                  
                1 - Fatura         ...
                2 - Funcionario    ...
                3 - Estatisticas   ...
       
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
            if op == "2":
                main_funcionarios()
            elif op == "1":
                main_fatura()
            elif op == "3":
                main_estatisticas()
            elif op == "v":
                break
        except mysql.connector.Error as err:
            print('Ups! Ocorreu um erro!')
            print(err.errno)
        else:
            cnx.close()
