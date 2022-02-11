from utils import *
import mysql.connector
from config import config
from tabulate import tabulate


def lista_categorias_preferidas(cnx):
    sql = """SELECT categoriaproduto.designacao, SUM(quantidade) as total FROM barcantina.produtofatura INNER JOIN produto
ON produtofatura.idproduto = produto.idproduto INNER JOIN categoriaproduto ON produto.idcategoria = categoriaproduto.idcategoriaProduto
group by categoriaproduto.designacao
order by total DESC"""
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['DesignaçãoCategoria', 'Total'], tablefmt='psql'))


def lista_categoriaprodutos(cnx):
    sql = """ SELECT * FROM categoriaproduto """
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['Id', 'NomeCategoria'], tablefmt='psql'))


def insere_categoriaprodutos(cnx):
    sql = """ INSERT  INTO  categoriaproduto (
                    idcategoriaProduto, 
                    designacao
                ) VALUES (
                    DEFAULT, 
                    %(DesignacaoCategoriaproduto)s
                )
        """

    data = dict()
    data["DesignacaoCategoriaproduto"] = input(f"Designacao Categoria produto? ")

    with cnx.cursor() as cursor:
        cursor.execute(sql, data)
        cnx.commit()
    print('Dado adicionado!')


def filtra_categoriaprodutos(cnx):
    print('''Pode filtrar as pesquisas por:
          Categoria do produto: (ex: Carne)
          Pelo Id da Categoria produto: (ex: 4)''')
    filtro = input("Filtro? ")
    data = 2 * (filtro,)  # sao 4 atributos
    sql = """ SELECT * FROM categoriaproduto
        WHERE idcategoriaProduto like %s
            Or designacao LIKE %s
            """
    # print(sql)

    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdCategoria', 'DesignacaoCategoria'], tablefmt='psql'))


def main_le_opcao():
    print(80 * "#")
    print("""                Menu Categoria Produtos\n
                    1 - Veja todos as categorias de produtos disponiveis na Universidade
                    2 - Filtre a categoria de produto que deseja ver (Id, Nome, Descrição)
                    3 - Adicione uma nova categoria de produto na base de dados
                    4 - Mostra a categoria de produtos preferida pelos estudantes

                 v - Voltar Menu Anterior
                 x - sair
            """)
    print(80 * "#")
    op = input("opção? ")
    print(80 * "#")
    return op


def main_categoriaprodutos():
    # try:
    cnx = mysql.connector.connect(**config)
    while True:
        op = main_le_opcao()
        if op == "1":  # lista todos os clientes
            lista_categoriaprodutos(cnx)
        elif op == "2":  # lista clientes que satisfazem o filtro
            filtra_categoriaprodutos(cnx)
        elif op == "3":  # insere um novo cliente
            insere_categoriaprodutos(cnx)
        elif op == "4":
            lista_categorias_preferidas(cnx)
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