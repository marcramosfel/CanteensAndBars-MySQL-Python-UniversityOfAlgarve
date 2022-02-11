from utils import *
import mysql.connector
from config import config
from tabulate import tabulate

#os produtos estão disponiveis globalmente ou seja sua disponibilidade é afetada em todos os bares!
#caso um produto não esteja disponivel, este não estara em todos os bares e cantina!
def lista_stockminimo_maior_stock(cnx):
    sql = """SELECT produtoespacoalimentar.idespacoAlimentar, espacoalimentar.nome as ne, produtoespacoalimentar.idproduto, produto.designacao as np, produtoespacoalimentar.stock,
    produtoespacoalimentar.stockminimo, (stockminimo-stock+1) as QuantidadeEncomendar  FROM produtoespacoalimentar INNER JOIN produto ON produto.idproduto = produtoespacoalimentar.idproduto
    INNER JOIN espacoalimentar ON espacoalimentar.idespacoAlimentar = produtoespacoalimentar.idespacoAlimentar 
    WHERE produtoespacoalimentar.stockminimo > produtoespacoalimentar.stock"""
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdBar', 'NomeBar', 'Idproduto', 'Nomeproduto', 'Stock', 'StockMinimo', 'Quantidade a encomendar'],
                   tablefmt='psql'))


    op = input('Deseja regularizar a situação de algum produto? s/n ')
    if op == "s":
        idespaco = input('Selecione de qual espaco alimentar quer regulamentar a situação dos produtos com stock menor que stock minimo? ')
        sql1 = """SELECT produtoespacoalimentar.idespacoAlimentar, espacoalimentar.nome as ne,
         produtoespacoalimentar.idproduto, produto.designacao as np, produtoespacoalimentar.stock,
            produtoespacoalimentar.stockminimo, (stockminimo-stock+1) as QuantidadeEncomendar 
             FROM produtoespacoalimentar INNER JOIN produto ON produto.idproduto = produtoespacoalimentar.idproduto
            INNER JOIN espacoalimentar ON espacoalimentar.idespacoAlimentar = produtoespacoalimentar.idespacoAlimentar 
            WHERE produtoespacoalimentar.stockminimo > produtoespacoalimentar.stock and produtoespacoalimentar.idespacoAlimentar like %s"""
        data1 = (idespaco,)
        cursor1 = cnx.cursor()
        cursor1.execute(sql1, data1)
        resultado = cursor1.fetchall()
        #print(resultado[0][4])
        print(tabulate(resultado, headers=['IdBar', 'NomeBar', 'Idproduto', 'Nomeproduto', 'Stock', 'StockMinimo',
                                           'Quantidade a encomendar'],
                       tablefmt='psql'))
        idproduto = input('Qual produto quer encomendar?')
        sql2 = f"""SELECT stock FROM produtoespacoalimentar  WHERE produtoespacoalimentar.stockminimo > produtoespacoalimentar.stock 
                    and produtoespacoalimentar.idespacoAlimentar = {idespaco} 
                    and produtoespacoalimentar.idproduto = {idproduto} """
        data2 = None
        cursor2 = cnx.cursor()
        cursor2.execute(sql2, data2)
        resultado1 = cursor2.fetchall()
        print(resultado1[0][0])
        #quantidadeaencomendar = cursor2.fetchall()
        #stockfinal = quantidadeaencomendar[0][0] + resultado[0][4]
        stockfinal = int(input("Qual a quantidade quer encomendar?")) + resultado1[0][0]
        #print(tabulate(quantidadeaencomendar, headers=['Quantidade a encomendar'], tablefmt='psql'))
        sql3 = """UPDATE produtoespacoalimentar SET produtoespacoalimentar.stock = %(stockfinal)s
        WHERE (produtoespacoalimentar.idespacoAlimentar = %(idespaco)s
        AND produtoespacoalimentar.idproduto = %(idproduto)s)"""
        data3 = {"stockfinal":stockfinal, "idespaco": idespaco, "idproduto":idproduto}
        cursor3 = cnx.cursor()
        cursor3.execute(sql3, data3)
        cnx.commit()
        print('Stock atualizado!')



def lista_stock_produto_espacoalimentar_especifico(cnx):
    filtro = input('Qual espaço alimentar quer consultar o stock?')
    data = 2*(filtro,)
    sql = """ SELECT produtoespacoalimentar.idespacoAlimentar, espacoalimentar.nome as ne, produtoespacoalimentar.idproduto, produto.designacao as np, produtoespacoalimentar.stock,
    produtoespacoalimentar.stockminimo 
    FROM produtoespacoalimentar INNER JOIN produto ON produto.idproduto = produtoespacoalimentar.idproduto
    INNER JOIN espacoalimentar ON espacoalimentar.idespacoAlimentar = produtoespacoalimentar.idespacoAlimentar
    WHERE (espacoalimentar.idespacoalimentar like %s
    OR espacoalimentar.nome like %s)"""

    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdBar', 'NomeBar', 'Idproduto','Nomeproduto', 'Stock', 'StockMinimo'], tablefmt='psql'))

def lista_stock_produto_espacoalimentar(cnx):
    sql = """ SELECT produtoespacoalimentar.idespacoAlimentar, espacoalimentar.nome as ne, 
    produtoespacoalimentar.idproduto, produto.designacao as np, produtoespacoalimentar.stock, produtoespacoalimentar.stockminimo 
    FROM produtoespacoalimentar INNER JOIN produto 
    ON produto.idproduto = produtoespacoalimentar.idproduto
    INNER JOIN espacoalimentar 
    ON espacoalimentar.idespacoAlimentar = produtoespacoalimentar.idespacoAlimentar
    WHERE produto.consumivel = 1"""

    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdBar', 'NomeBar', 'Idproduto','Nomeproduto', 'Stock', 'StockMinimo'], tablefmt='psql'))

def lista_preco_produto_espacoalimentar_especifico(cnx):
    filtro = input('Qual espaço alimentar quer consultar os preços?')
    data = 2*(filtro,)
    sql = """ SELECT produtoespacoalimentar.idespacoAlimentar, espacoalimentar.nome as ne, produtoespacoalimentar.idproduto, produto.designacao as np, produtoespacoalimentar.preco 
    FROM produtoespacoalimentar INNER JOIN produto ON produto.idproduto = produtoespacoalimentar.idproduto
    INNER JOIN espacoalimentar ON espacoalimentar.idespacoAlimentar = produtoespacoalimentar.idespacoAlimentar
    WHERE (espacoalimentar.idespacoalimentar like %s
    OR espacoalimentar.nome like %s) AND produto.consumivel = 1"""

    cursor = cnx.cursor()
    cursor.execute(sql, data)

    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdBar', 'NomeBar', 'Idproduto','Nomeproduto', 'Preço'], tablefmt='psql'))

def lista_preco_produto_espacoalimentar_especifico_2(cnx, idea):
    filtro = idea
    data = 2*(filtro,)
    sql = """ SELECT produtoespacoalimentar.idespacoAlimentar, espacoalimentar.nome as ne, produtoespacoalimentar.idproduto, produto.designacao as np, produtoespacoalimentar.preco 
    FROM produtoespacoalimentar INNER JOIN produto ON produto.idproduto = produtoespacoalimentar.idproduto
    INNER JOIN espacoalimentar ON espacoalimentar.idespacoAlimentar = produtoespacoalimentar.idespacoAlimentar
    WHERE (espacoalimentar.idespacoalimentar like %s
    OR espacoalimentar.nome like %s) AND produto.consumivel = 1"""

    cursor = cnx.cursor()
    cursor.execute(sql, data)

    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdBar', 'NomeBar', 'Idproduto','Nomeproduto', 'Preço'], tablefmt='psql'))



def lista_preco_produto_espacoalimentar(cnx):
    sql = """ SELECT produtoespacoalimentar.idespacoAlimentar, espacoalimentar.nome as ne, 
    produtoespacoalimentar.idproduto, produto.designacao as np, produtoespacoalimentar.preco 
    FROM produtoespacoalimentar INNER JOIN produto 
    ON produto.idproduto = produtoespacoalimentar.idproduto
    INNER JOIN espacoalimentar 
    ON espacoalimentar.idespacoAlimentar = produtoespacoalimentar.idespacoAlimentar
    WHERE produto.consumivel = 1"""

    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdBar', 'NomeBar', 'Idproduto','Nomeproduto', 'Preço'], tablefmt='psql'))

def insere_produto_preco(cnx):
    print('INSIRA O ID DO produto E O RESPECTIVO ID DO ESPACO ALIMENTAR QUE IRÁ PASSAR A VENDER ESSE produto. EM SEGUIDA INSIRA O PREÇO DO produto')
    sql_mostra_produtos = """ SELECT idproduto, designacao FROM produto WHERE produto.consumivel = 1"""
    data2 = None

    sql_mostra_espaco = """ SELECT idespacoAlimentar, nome FROM espacoalimentar"""
    sql = """ INSERT  INTO produtoespacoalimentar (
                    idespacoAlimentar, 
                    idproduto, 
                    preco
                ) VALUES (
                    %(IdDoEspacoAlimentar)s, 
                    %(IdDoproduto)s, 
                    %(Preco)s
                )
        """

    print('\nLista com todos os produtos!\n\n')
    filtra_e_lista(cnx, data2, sql_mostra_produtos)
    print('\n\nLista com todos os espacos!\n\n')
    filtra_e_lista(cnx, data2, sql_mostra_espaco)
    print('\n\n')

    data = dict()
    for atributo in ("IdDoEspacoAlimentar", "IdDoproduto", "Preco"):
        data[atributo] = input(f"{atributo}? ")
    try:
        with cnx.cursor() as cursor:
            cursor.execute(sql, data)
            cnx.commit()
        print('Dado adicionado')
    except:
        print('''\nNão Possivel adicionar esse produto no espaco selecionado pois o espaco ja vende esse produto.
Caso pretenda mudar o preco selecione a opçao correta!\n''')
        pass

def alterar_preco(cnx):
    print("Pode alterar o preço de um produto ja existente em um bar que ja vende esse produto!")

    espaco_alimentar_alterar_preco = (input('Qual espaco alimentar quer alterar o preço?'))
    data2 = 2 * (espaco_alimentar_alterar_preco,)
    sql2 = """ SELECT produtoespacoalimentar.idespacoAlimentar, espacoalimentar.nome as ne, produtoespacoalimentar.idproduto, produto.designacao as np, produtoespacoalimentar.preco 
        FROM produtoespacoalimentar INNER JOIN produto ON produto.idproduto = produtoespacoalimentar.idproduto
        INNER JOIN espacoalimentar ON espacoalimentar.idespacoAlimentar = produtoespacoalimentar.idespacoAlimentar
        WHERE espacoalimentar.idespacoalimentar like %s
        OR espacoalimentar.nome like %s AND produto.consumivel = 1"""

    cursor2 = cnx.cursor()
    cursor2.execute(sql2, data2)
    resultado2 = cursor2.fetchall()
    print(tabulate(resultado2, headers=['IdBar', 'NomeBar', 'Idproduto', 'Nomeproduto', 'Preço'], tablefmt='psql'))

    sql = """UPDATE produtoespacoalimentar
        SET preco = %(preco)s
        WHERE (idespacoAlimentar = %(idespacoAlimentar)s and idproduto = %(idproduto)s)
       """
    data = dict()
    for atributo in ("idproduto", "preco"):
        data[atributo] = input(f"{atributo}? ")
    data["idespacoAlimentar"] = espaco_alimentar_alterar_preco
    with cnx.cursor() as cursor:
        cursor.execute(sql, data)
        cnx.commit()
    print('Preço Alterado com Sucesso')

def compare_precos(cnx):
    print('''Pode comparar os precos do mesmo produto dependendo do espaço alimentar!'''),
    filtro = input("Filtro? ")
    data = 3 * (filtro,) # sao 3 atributos
    sql = """ SELECT produtoespacoalimentar.idespacoAlimentar, espacoalimentar.nome, produtoespacoalimentar.idproduto, produto.designacao, produtoespacoalimentar.preco FROM produtoespacoalimentar
INNER JOIN produto ON produto.idproduto = produtoespacoalimentar.idproduto
INNER JOIN espacoalimentar ON espacoalimentar.idespacoAlimentar = produtoespacoalimentar.idespacoAlimentar
WHERE produto.idproduto LIKE %s
OR produto.designacao LIKE %s
OR espacoalimentar.nome LIKE %s
AND produto.consumivel = 1
order by idproduto
            """
    # print(sql)

    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdEspacoAlimentar', 'NomeEspaco', 'Idproduto', 'Nomeproduto', 'Preço'], tablefmt='psql'))

def espaco_com_preco_mais_baixo_de_certo_produto(cnx):
    print('''Aqui pode saber qual o lugar mais barato para um produto especifico usando o nome do produto ou o ID do produto\n''')
    filtro = input("Filtro? ")
    data = 2 * (filtro,) # sao 3 atributos
    sql = """SELECT produtoespacoalimentar.idespacoAlimentar, espacoalimentar.nome, produtoespacoalimentar.idproduto, produto.designacao, min(produtoespacoalimentar.preco) FROM produtoespacoalimentar
INNER JOIN produto ON produto.idproduto = produtoespacoalimentar.idproduto
INNER JOIN espacoalimentar ON espacoalimentar.idespacoAlimentar = produtoespacoalimentar.idespacoAlimentar
WHERE produto.designacao LIKE %s
OR produto.idproduto LIKE %s
AND produto.consumivel = 1

"""
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdEspacoAlimentar', 'NomeEspaco', 'Idproduto', 'Nomeproduto', 'Preço'], tablefmt='psql'))

def main_le_opcao():
    print(80 * "#")
    print("""                Menu Preços dos Produtos Dependendo dos Bares\n
                    1 - Veja todos os preços dos produtos organizados por espaço alimentar.
                    2 - Liste os produtos e compare os preços conforme o filtro que deseja usar:
                             (id do produto, nome do produto, nome do espaco alimentar)
                    3 - Aqui pode saber qual espaco vende o produto que deseja pelo menor valor.
                    4 - Inserir um produto ja existente em um espaco alimentar e seu respectivo
                              preço, caso este espaco alimentar passe a vender o produto.
                    5 - Alterar o preco de um produto.
                    6 - Veja os preços de um bar em especifico.
                    7 - Veja o stock e o stock minimo dos produtos por espaço alimentar 
                    8 - Veja o stock e o stock minimo dos produtos de um espaçoo alimentar especifico
                    9 - Veja quais produtos estao com stock abaixo do stock minimo
                    
                 v - Voltar Menu Anterior
                 x - sair
            """)
    print(80 * "#")
    op = input("opção? ")
    print(80 * "#")
    return op

def main_preco_produto_espacoalimentar():
    # try:
    cnx = mysql.connector.connect(**config)
    while True:
        op = main_le_opcao()
        if op == "1":  # lista todos os clientes
            lista_preco_produto_espacoalimentar(cnx)
        elif op == "2":  # lista clientes que satisfazem o filtro
            compare_precos(cnx)
        elif op == "3":  # insere um novo cliente
            espaco_com_preco_mais_baixo_de_certo_produto(cnx)
        elif op == "4":
            insere_produto_preco(cnx)
        elif op == "5":
            alterar_preco(cnx)
        elif op == "6":
            lista_preco_produto_espacoalimentar_especifico(cnx)
        elif op == "7":
            lista_stock_produto_espacoalimentar(cnx)
        elif op == "8":
            lista_stock_produto_espacoalimentar_especifico(cnx)
        elif op == "9":
            lista_stockminimo_maior_stock(cnx)
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