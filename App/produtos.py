from utils import *
import mysql.connector
from config import config
from tabulate import tabulate

def lista_todos_produtos(cnx):
    sql = """ SELECT 
        idproduto,
        produto.designacao,
        CONCAT(categoriaproduto.idcategoriaProduto,
                ' - ',
                categoriaproduto.designacao) AS nomeCategoria
    FROM
        produto
            INNER JOIN
        categoriaproduto ON categoriaproduto.idcategoriaProduto = produto.idcategoria
    ORDER BY idproduto"""
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['Id', 'Nome', 'NomeCategoria'], tablefmt='psql'))


def lista_produtos_mais_vendidos(cnx):
    sql = """SELECT 
    produto.idproduto,
    produto.designacao,
    categoriaproduto.designacao,
    SUM(quantidade) AS total
FROM
    barcantina.produtofatura
        INNER JOIN
    produto ON produtofatura.idproduto = produto.idproduto
        INNER JOIN
    categoriaproduto ON produto.idcategoria = categoriaproduto.idcategoriaproduto
GROUP BY idproduto
ORDER BY total DESC"""
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['Idproduto', 'Nomeproduto', 'Categoria', 'TotalVendido'], tablefmt='psql'))


def apaga_produto(cnx):
    sql = """ UPDATE produto SET consumivel = '0' WHERE (idproduto = %(idproduto)s) """
    atributo = input(f"idproduto?")
    data = {"idproduto": atributo}

    with cnx.cursor() as cursor:
        cursor.execute(sql, data)
        cnx.commit()
    print('produto removido')


def lista_produtos_nao_vendaveis(cnx):
    sql = """ SELECT 
    idproduto,
    produto.designacao,
    CONCAT(categoriaproduto.idcategoriaProduto,
            ' - ',
            categoriaproduto.designacao) AS nomeCategoria
FROM
    produto
        INNER JOIN
    categoriaproduto ON categoriaproduto.idcategoriaProduto = produto.idcategoria
WHERE
    produto.consumivel = 0
ORDER BY idproduto"""
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['Id', 'Nome', 'NomeCategoria'], tablefmt='psql'))

def lista_produtos_vendaveis(cnx):
    sql = """ SELECT 
    idproduto,
    produto.designacao,
    CONCAT(categoriaproduto.idcategoriaProduto,
            ' - ',
            categoriaproduto.designacao) AS nomeCategoria
FROM
    produto
        INNER JOIN
    categoriaproduto ON categoriaproduto.idcategoriaProduto = produto.idcategoria
WHERE
    produto.consumivel = 1
ORDER BY idproduto"""
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['Id', 'Nome', 'NomeCategoria'], tablefmt='psql'))



def insere_produtos(cnx):
    sql = """ INSERT  INTO  produto (
                    idproduto, 
                    designacao, 
                    consumivel, 
                    idcategoria
                    
                ) VALUES (
                    DEFAULT, 
                    %(NomeDoProduto)s, 
                    %(consumivel)s,
                    %(IdCategoria)s
                )
        """
    print('Tenha Atenção ao colocar o id da categoria do produto\n Certifique-se que o produto que irá adicionar'
          'está dentro da categoria certa!')

    # orienta o utilizador a saber qual id colocar!
    sql2 = """SELECT * FROM categoriaproduto"""
    data2 = None
    filtra_e_lista(cnx, data2, sql2)

    data = dict()
    for atributo in ("NomeDoProduto", "IdCategoria"):
        data[atributo] = input(f"{atributo}? ")
    vendavel_or_consumivel = input('O produto que irá adicionar é Vendavel(1) ou Consumível(0)')
    data["consumivel"] = int(vendavel_or_consumivel)

    with cnx.cursor() as cursor:
        cursor.execute(sql, data)
        cnx.commit()
    print('Dado adicionado')


def filtra_produtos(cnx):
    print('''Pode filtrar as pesquisas por:
          Nome do produto: (ex: Chicletes)
          Categoria do produto: (ex: Snack)
          Pelo Id Do produto: (ex: 4)''')
    filtro = input("Filtro? ")
    data = 3 * (filtro,)  # sao 4 atributos
    sql = """ SELECT 
    produto.idproduto,
    produto.designacao,
    categoriaproduto.designacao,
    produto.consumivel
FROM
    produto
        INNER JOIN
    categoriaproduto ON produto.idcategoria= categoriaproduto.idcategoriaProduto
    WHERE produto.idproduto like %s
            OR produto.designacao like %s
            Or categoriaproduto.designacao LIKE %s
            """
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    if resultado == []:
        print(f"Nao foi encontrado o filtro `{filtro}´ nas pesquisas de produtos!")
    else:
        print(tabulate(resultado, headers=['Idproduto', 'NomeDoproduto', 'NomeCategoria', 'Consumivel'],
                       tablefmt='psql'))

    '''if filtra_e_lista(cnx, data, sql) == 0:
        print(f'Nao encontrado o filtro {filtro}')'''



def main_le_opcao():
    print(80 * "#")
    print("""                Menu dos Produtos\n
                    1 - Veja todos os produtos vendáveis na Universidade.
                    2 - Filtre o produto que deseja ver (Id, Nome, Categoria).
                    3 - Adicione um novo produto na base de dados.
                    4 - Remover produto, passando-o para não vendável. 
                    5 - Lista os produtos que não são vendáveis ao público.
                    6 - Lista dos produtos mais vendidos na Universidade desde sempre.
                    7 - Lista todos os produtos, tanto os vendaveis como os consumivéis!
                    
                 v - Voltar Menu Anterior
                 x - sair
            """)
    print(80 * "#")
    op = input("opção? ")
    print(80 * "#")
    return op


def main_produtos():
    # try:
    cnx = mysql.connector.connect(**config)
    while True:
        op = main_le_opcao()
        if op == "1":  # lista todos os clientes
            lista_produtos_vendaveis(cnx)
        elif op == "2":  # lista clientes que satisfazem o filtro
            filtra_produtos(cnx)
        elif op == "3":  # insere um novo cliente
            insere_produtos(cnx)
        elif op == "4":
            apaga_produto(cnx)
        elif op == "5":
            lista_produtos_nao_vendaveis(cnx)
        elif op == "6":
            lista_produtos_mais_vendidos(cnx)
        elif op == "7":
            lista_todos_produtos(cnx)
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