from utils import *
import mysql.connector
from config import config
from tabulate import tabulate

#os pratos estão disponiveis globalmente ou seja sua disponibilidade é afetada em todos os bares!
#caso um prato não esteja disponivel, este não estara em todos os bares e cantina!
def lista_preco_prato_espacoalimentar_especifico(cnx):
    filtro = input('Qual espaço alimentar quer consultar os preços?')
    data = 2*(filtro,)
    sql = """ SELECT pratoespacoalimentar.idespacoAlimentar, espacoalimentar.nome as ne, pratoespacoalimentar.idprato, prato.nome as np, pratoespacoalimentar.preco 
    FROM pratoespacoalimentar INNER JOIN prato ON prato.idprato = pratoespacoalimentar.idprato
    INNER JOIN espacoalimentar ON espacoalimentar.idespacoAlimentar = pratoespacoalimentar.idespacoAlimentar
    WHERE espacoalimentar.idespacoalimentar like %s
    OR espacoalimentar.nome like %s AND prato.vendavel = 1"""

    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdBar', 'NomeBar', 'IdPrato','NomePrato', 'Preço'], tablefmt='psql'))


def lista_preco_prato_espacoalimentar_especifico_2(cnx, idea):
    filtro = idea
    data = 2*(filtro,)
    sql = """ SELECT pratoespacoalimentar.idespacoAlimentar, espacoalimentar.nome as ne, pratoespacoalimentar.idprato, prato.nome as np, pratoespacoalimentar.preco 
    FROM pratoespacoalimentar INNER JOIN prato ON prato.idprato = pratoespacoalimentar.idprato
    INNER JOIN espacoalimentar ON espacoalimentar.idespacoAlimentar = pratoespacoalimentar.idespacoAlimentar
    WHERE espacoalimentar.idespacoalimentar like %s
    OR espacoalimentar.nome like %s AND prato.vendavel = 1"""

    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdBar', 'NomeBar', 'IdPrato','NomePrato', 'Preço'], tablefmt='psql'))

def lista_preco_prato_espacoalimentar(cnx):
    sql = """ SELECT pratoespacoalimentar.idespacoAlimentar, espacoalimentar.nome as ne, 
    pratoespacoalimentar.idprato, prato.nome as np, pratoespacoalimentar.preco 
    FROM pratoespacoalimentar INNER JOIN prato 
    ON prato.idprato = pratoespacoalimentar.idprato
    INNER JOIN espacoalimentar 
    ON espacoalimentar.idespacoAlimentar = pratoespacoalimentar.idespacoAlimentar
    WHERE prato.vendavel = 1"""

    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdBar', 'NomeBar', 'IdPrato','NomePrato', 'Preço'], tablefmt='psql'))

def insere_prato_preco(cnx):
    print('INSIRA O ID DO PRATO E O RESPECTIVO ID DO ESPACO ALIMENTAR QUE IRÁ PASSAR A VENDER ESSE PRATO. EM SEGUIDA INSIRA O PREÇO DO PRATO')
    sql_mostra_pratos = """ SELECT idprato, nome FROM prato WHERE prato.vendavel = 1"""
    data2 = None

    sql_mostra_espaco = """ SELECT idespacoAlimentar, nome FROM espacoalimentar"""
    sql = """ INSERT  INTO pratoespacoalimentar (
                    idespacoAlimentar, 
                    idprato, 
                    preco
                ) VALUES (
                    %(IdDoEspacoAlimentar)s, 
                    %(IdDoPrato)s, 
                    %(Preco)s
                )
        """

    print('\nLista com todos os pratos!\n\n')
    filtra_e_lista(cnx, data2, sql_mostra_pratos)
    print('\n\nLista com todos os espacos!\n\n')
    filtra_e_lista(cnx, data2, sql_mostra_espaco)
    print('\n\n')

    data = dict()
    for atributo in ("IdDoEspacoAlimentar", "IdDoPrato", "Preco"):
        data[atributo] = input(f"{atributo}? ")
    try:
        with cnx.cursor() as cursor:
            cursor.execute(sql, data)
            cnx.commit()
        print('Dado adicionado')
    except:
        print('''\nNão Possivel adicionar esse prato no espaco selecionado pois o espaco ja vende esse prato.
Caso pretenda mudar o preco selecione a opçao correta!\n''')
        pass

def alterar_preco(cnx):
    print("Pode alterar o preço de um prato ja existente em um bar que ja vende esse prato!")

    espaco_alimentar_alterar_preco = (input('Qual espaco alimentar quer alterar o preço?'))
    data2 = 2 * (espaco_alimentar_alterar_preco,)
    sql2 = """ SELECT pratoespacoalimentar.idespacoAlimentar, espacoalimentar.nome as ne, pratoespacoalimentar.idprato, prato.nome as np, pratoespacoalimentar.preco 
        FROM pratoespacoalimentar INNER JOIN prato ON prato.idprato = pratoespacoalimentar.idprato
        INNER JOIN espacoalimentar ON espacoalimentar.idespacoAlimentar = pratoespacoalimentar.idespacoAlimentar
        WHERE espacoalimentar.idespacoalimentar like %s
        OR espacoalimentar.nome like %s AND prato.vendavel = 1"""

    cursor2 = cnx.cursor()
    cursor2.execute(sql2, data2)
    resultado2 = cursor2.fetchall()
    print(tabulate(resultado2, headers=['IdBar', 'NomeBar', 'IdPrato', 'NomePrato', 'Preço'], tablefmt='psql'))

    sql = """UPDATE pratoespacoalimentar
        SET preco = %(preco)s
        WHERE (idespacoAlimentar = %(idespacoAlimentar)s and idprato = %(idprato)s)
       """
    data = dict()
    for atributo in ("idprato", "preco"):
        data[atributo] = input(f"{atributo}? ")
    data["idespacoAlimentar"] = espaco_alimentar_alterar_preco
    with cnx.cursor() as cursor:
        cursor.execute(sql, data)
        cnx.commit()
    print('Preço Alterado com Sucesso')

def compare_precos(cnx):
    print('''Pode comparar os precos do mesmo prato dependendo do espaço alimentar!'''),
    filtro = input("Filtro? ")
    data = 3 * (filtro,) # sao 3 atributos
    sql = """ SELECT pratoespacoalimentar.idespacoAlimentar, espacoalimentar.nome, pratoespacoalimentar.idprato, prato.nome, pratoespacoalimentar.preco FROM pratoespacoalimentar
INNER JOIN prato ON prato.idprato = pratoespacoalimentar.idprato
INNER JOIN espacoalimentar ON espacoalimentar.idespacoAlimentar = pratoespacoalimentar.idespacoAlimentar
WHERE prato.idprato LIKE %s
OR prato.nome LIKE %s
OR espacoalimentar.nome LIKE %s
AND prato.vendavel = 1
order by idprato
            """
    # print(sql)

    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdEspacoAlimentar', 'NomeEspaco', 'IdPrato', 'NomePrato', 'Preço'], tablefmt='psql'))

def espaco_com_preco_mais_baixo_de_certo_prato(cnx):
    print('''Aqui pode saber qual o lugar mais barato para um prato especifico usando o nome do prato ou o ID do prato\n''')
    filtro = input("Filtro? ")
    data = 2 * (filtro,) # sao 3 atributos
    sql = """SELECT pratoespacoalimentar.idespacoAlimentar, espacoalimentar.nome, pratoespacoalimentar.idprato, prato.nome, min(pratoespacoalimentar.preco) FROM pratoespacoalimentar
INNER JOIN prato ON prato.idprato = pratoespacoalimentar.idprato
INNER JOIN espacoalimentar ON espacoalimentar.idespacoAlimentar = pratoespacoalimentar.idespacoAlimentar
WHERE prato.nome LIKE %s
OR prato.idprato LIKE %s
AND prato.vendavel = 1

"""
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdEspacoAlimentar', 'NomeEspaco', 'IdPrato', 'NomePrato', 'Preço'], tablefmt='psql'))

def main_le_opcao():
    print(80 * "#")
    print("""                Menu Preços dos Pratos Dependendo dos Bares\n
                    1 - Veja todos os preços dos pratos organizados por espaço alimentar
                    2 - Liste os pratos e compare os preços conforme o filtro que deseja usar:
                             (id do prato, nome do prato, nome do espaco alimentar)
                    3 - Aqui pode saber qual espaco vende o prato que deseja pelo menor valor.
                    4 - Inserir um prato ja existente em um espaco alimentar e seu respectivo
                              preço, caso este espaco alimentar passe a vender o prato.
                    5 - Alterar o preco de um prato.
                    6 - Veja os preços de um bar em especifico. 

                 v - Voltar Menu Anterior
                 x - sair
            """)
    print(80 * "#")
    op = input("opção? ")
    print(80 * "#")
    return op

def main_preco_prato_espacoalimentar():
    # try:
    cnx = mysql.connector.connect(**config)
    while True:
        op = main_le_opcao()
        if op == "1":  # lista todos os clientes
            lista_preco_prato_espacoalimentar(cnx)
        elif op == "2":  # lista clientes que satisfazem o filtro
            compare_precos(cnx)
        elif op == "3":  # insere um novo cliente
            espaco_com_preco_mais_baixo_de_certo_prato(cnx)
        elif op == "4":
            insere_prato_preco(cnx)
        elif op == "5":
            alterar_preco(cnx)
        elif op == "6":
            lista_preco_prato_espacoalimentar_especifico(cnx)
        elif op == "x":
            exit()
        elif op == "v":
            print('Voltando...')
            break
    # except mysql.connector.Error as err:
    #     print('Ups! Ocorreu um erro!')
    #     print(err.errno)
    # else:
    cnx.close()