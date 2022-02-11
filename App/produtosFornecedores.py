import decimal
import mysql.connector
from config import config
from tabulate import tabulate
from produtos import lista_todos_produtos


def mostra_produtos_disponiveis_por_fornecedor(cnx,filtro):

    data = 2 * (filtro,)  # sao 2 atributos
    sql = """ SELECT 
        fornecedor_has_produto.fornecedor_idfornecedor,
        fornecedor.nome,
        fornecedor_has_produto.produto_idproduto,
        produto.designacao,
        fornecedor_has_produto.preco
    FROM
        fornecedor_has_produto
            INNER JOIN
        fornecedor ON fornecedor_has_produto.fornecedor_idfornecedor = fornecedor.idfornecedor
            INNER JOIN
        produto ON fornecedor_has_produto.produto_idproduto = produto.idproduto
    WHERE produto.idproduto LIKE %s
    OR produto.designacao LIKE %s

    ORDER BY fornecedor_has_produto.fornecedor_idfornecedor"""
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdFornecedor',
                                       'NomeFornecedor',
                                       'IdProduto', 'Designacao', 'Preço'], tablefmt='psql'))


def lista_produtos_fornecidos_por_cada_fornecedor(cnx):
    sql = """SELECT 
    fornecedor_idfornecedor,
    fornecedor.nome,
    produto_idproduto,
    produto.designacao,
    preco
FROM
    barcantina.fornecedor_has_produto
        INNER JOIN
    fornecedor ON fornecedor_has_produto.fornecedor_idfornecedor = fornecedor.idfornecedor
        INNER JOIN
    produto ON fornecedor_has_produto.produto_idproduto = produto.idproduto
    
ORDER BY fornecedor_idfornecedor"""
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdFornecedor',
                                       'NomeFornecedor',
                                       'IdProduto', 'Designacao','Preço'], tablefmt='psql'))


def lista_produto_mais_barato_por_fornecedor(cnx):
    print('''Pode filtrar pelo ID do Produto ou pelo nome do produto''')
    filtro = input("Filtro? ")
    data = 2 * (filtro,)  # sao 2 atributos
    sql = """ SELECT 
    fornecedor_has_produto.fornecedor_idfornecedor,
    fornecedor.nome,
    fornecedor_has_produto.produto_idproduto,
    produto.designacao,
    min(fornecedor_has_produto.preco)
FROM
    fornecedor_has_produto
        INNER JOIN
    fornecedor ON fornecedor_has_produto.fornecedor_idfornecedor = fornecedor.idfornecedor
        INNER JOIN
    produto ON fornecedor_has_produto.produto_idproduto = produto.idproduto
WHERE produto.idproduto LIKE %s
OR produto.designacao LIKE %s
    
ORDER BY fornecedor_has_produto.fornecedor_idfornecedor"""
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdFornecedor',
                                       'NomeFornecedor',
                                       'IdProduto', 'Designacao', 'Preço'], tablefmt='psql'))


def realiza_encomenda(cnx):
    continuar_encomenda = True
    resultado2 = 0.0 # variavel iniciada para ser ancora na soma dos valores
    while continuar_encomenda == True:
        print('''Aqui pode simular o valor de uma encomenda de vários produtos com diferentes fornecedores
        Em primeiro lugar escolha um produto disponivel da lista de produtos:''')
        lista_todos_produtos(cnx)
        filtro_produto = input('Qual o id do produto ou nome do produto que quer encomendar?')
        mostra_produtos_disponiveis_por_fornecedor(cnx,filtro_produto)
        filtro_fornecedor = input('Qual o id do Fornecedor que quer encomendar')
        quantidade = int(input('Qual a quantidade quer encomendar desse produto'))
        sql = """ SELECT 
        (preco * %(quantidade)s)
    FROM
        fornecedor_has_produto
    where fornecedor_idfornecedor like %(filtro_fornecedor)s AND produto_idproduto like %(filtro_produto)s """
        data = {"quantidade":quantidade, "filtro_fornecedor":filtro_fornecedor, "filtro_produto": filtro_produto }
        cursor = cnx.cursor()
        cursor.execute(sql, data)
        resultado = cursor.fetchall()
        resultado1 = resultado[0][0]
        continuar = input('Continuar encomenda?')
        if continuar == 's':
            print(type(resultado1)) #decimal.Decimal
            resultado2 = decimal.Decimal(resultado2) + decimal.Decimal(resultado1)

            print(tabulate([[resultado2]], headers=['PreçoTotal'], tablefmt='psql'))
#            print(resultado2)
            continue
        else:
            continuar_encomenda = False

def main_le_opcao():
    print(80 * "#")
    print("""                Menu Preços dos Produtos Dependendo dos Fornecedores\n
                    1 - Veja todos os produtos fornecidos por cada fornecedor.
                    2 - Liste o fornecedor que fornece um determinado produto pelo preço mais baixo.
                    3 - Simula o valor de uma encomenda.
                    4 - Mostra os fornecedores que fornecem esse produto.

                 v - Voltar Menu Anterior
                 x - sair
            """)
    print(80 * "#")
    op = input("opção? ")
    print(80 * "#")
    return op


def main_produtos_fornecedores():
    # try:
    cnx = mysql.connector.connect(**config)
    while True:
        op = main_le_opcao()
        if op == "1":
            lista_produtos_fornecidos_por_cada_fornecedor(cnx)
        elif op == "2":
            lista_produto_mais_barato_por_fornecedor(cnx)
        elif op == "3":
            realiza_encomenda(cnx)
        elif op == "4":
            print('''Pode filtrar pelo ID do Produto ou pelo nome do produto''')
            filtro = input("Filtro? ")
            mostra_produtos_disponiveis_por_fornecedor(cnx, filtro)
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