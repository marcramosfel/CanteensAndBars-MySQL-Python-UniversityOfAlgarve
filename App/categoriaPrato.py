from utils import *
import mysql.connector
from config import config
from tabulate import tabulate

def lista_categorias_preferidas(cnx):
    sql = """SELECT categoriaprato.designacao, SUM(quantidade) as total FROM barcantina.pratofatura INNER JOIN prato
ON pratofatura.idprato = prato.idprato INNER JOIN categoriaprato ON prato.idcategoriaPrato = categoriaprato.idcategoriaPrato
group by categoriaprato.designacao
order by total DESC"""
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['DesignaçãoCategoria', 'Total'], tablefmt='psql'))
def lista_categoriaPratos(cnx):
    sql = """ SELECT * FROM categoriaprato """
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['Id','NomeCategoria'], tablefmt='psql'))

def insere_categoriaPratos(cnx):
    sql = """ INSERT  INTO  categoriaprato (
                    idcategoriaPrato, 
                    designacao
                ) VALUES (
                    DEFAULT, 
                    %(DesignacaoCategoriaPrato)s
                )
        """

    data = dict()
    data["DesignacaoCategoriaPrato"] = input(f"Designacao Categoria Prato? ")

    with cnx.cursor() as cursor:
        cursor.execute(sql, data)
        cnx.commit()
    print('Dado adicionado!')

def filtra_categoriaPratos(cnx):
    print('''Pode filtrar as pesquisas por:
          Categoria do Prato: (ex: Carne)
          Pelo Id da Categoria Prato: (ex: 4)''')
    filtro = input("Filtro? ")
    data = 2 * (filtro,) #sao 4 atributos
    sql = """ SELECT * FROM categoriaprato
        WHERE idcategoriaPrato like %s
            Or designacao LIKE %s
            """
    #print(sql)

    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdCategoria','DesignacaoCategoria'], tablefmt='psql'))
def main_le_opcao():
    print(80 * "#")
    print("""                Menu Categoria Pratos\n
                    1 - Veja todos as categorias de pratos disponiveis na Universidade
                    2 - Filtre a categoria de prato que deseja ver (Id, Nome, Descrição)
                    3 - Adicione uma nova categoria de prato na base de dados
                    4 - Mostra a categoria de pratos preferida pelos estudantes
                    
                 v - Voltar Menu Anterior
                 x - sair
            """)
    print(80 * "#")
    op = input("opção? ")
    print(80 * "#")
    return op

def main_categoriaPratos():
    # try:
    cnx = mysql.connector.connect(**config)
    while True:
        op = main_le_opcao()
        if op == "1":  # lista todos os clientes
            lista_categoriaPratos(cnx)
        elif op == "2":  # lista clientes que satisfazem o filtro
            filtra_categoriaPratos(cnx)
        elif op == "3":  # insere um novo cliente
            insere_categoriaPratos(cnx)
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