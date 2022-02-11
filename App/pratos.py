from utils import *
import mysql.connector
from config import config
from tabulate import tabulate





def lista_pratos_mais_vendidos(cnx):
    sql = """SELECT prato.idprato, prato.nome, categoriaprato.designacao, SUM(quantidade) as total 
    FROM barcantina.pratofatura INNER JOIN prato ON pratofatura.idprato = prato.idprato 
    INNER JOIN categoriaprato ON prato.idcategoriaPrato = categoriaprato.idcategoriaPrato
    group by idprato
    order by total DESC"""
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdPrato', 'NomePrato', 'Categoria', 'TotalVendido'], tablefmt='psql'))
def mostra_pratos_nao_disponiveis(cnx):
    sql = """ SELECT idprato, nome, descricao, CONCAT(categoriaprato.idcategoriaPrato, ' - ', categoriaprato.designacao) as nomeCategoria FROM prato 
    INNER JOIN categoriaprato ON categoriaprato.idcategoriaPrato = prato.idcategoriaPrato 
    WHERE prato.vendavel = 0"""
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['Id', 'Nome', 'Descricao', 'NomeCategoria'], tablefmt='psql'))

def apaga_prato(cnx):
    sql = """ UPDATE prato SET vendavel = '0' WHERE (idprato = %(idprato)s) """
    atributo = input(f"idprato?")
    data = {"idprato" : atributo}

    with cnx.cursor() as cursor:
        cursor.execute(sql, data)
        cnx.commit()
    print('Prato removido')

def lista_pratos(cnx):
    sql = """ SELECT idprato, nome, descricao, CONCAT(categoriaprato.idcategoriaPrato, ' - ', categoriaprato.designacao) as nomeCategoria FROM prato 
INNER JOIN categoriaprato ON categoriaprato.idcategoriaPrato = prato.idcategoriaPrato 
WHERE prato.vendavel = 1 ORDER BY idprato"""
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(resultado)
    print(tabulate(resultado, headers=['Id', 'Nome', 'Descricao','NomeCategoria'], tablefmt='psql'))

def insere_pratos(cnx):
    sql = """ INSERT  INTO  prato (
                    idPrato, 
                    nome, 
                    descricao, 
                    idcategoriaPrato,
                    vendavel
                ) VALUES (
                    DEFAULT, 
                    %(NomeDoPrato)s, 
                    %(DescricaoDoPrato)s, 
                    %(IdCategoriaDoPrato)s,
                    %(vendavel)s
                )
        """
    print('Tenha Atenção ao colocar o id da categoria do prato\n Certifique-se que o prato que irá adicionar'
          'está dentro da categoria certa!')

    #orienta o utilizador a saber qual id colocar!
    sql2= """SELECT * FROM categoriaprato"""
    data2 = None
    filtra_e_lista(cnx, data2, sql2)

    data = dict()
    for atributo in ("NomeDoPrato", "DescricaoDoPrato", "IdCategoriaDoPrato"):
        data[atributo] = input(f"{atributo}? ")
    data["vendavel"] = 1

    with cnx.cursor() as cursor:
        cursor.execute(sql, data)
        print(sql)
        #cnx.commit()
    print('Dado adicionado')

def filtra_pratos(cnx):
    print('''Pode filtrar as pesquisas por:
          Nome do Prato: (ex: Carbonara)
          Categoria do Prato: (ex: Carne)
          Pela descrição: (ex: As lentilhas são leguminosas muito nutritivas)
          Pelo Id Do Prato: (ex: 4)''')
    filtro = input("Filtro? ")
    data = 4 * (filtro,) #sao 4 atributos
    sql = """ SELECT prato.idPrato, prato.nome, prato.descricao, categoriaprato.designacao 
        FROM prato INNER JOIN categoriaprato ON prato.idcategoriaPrato = categoriaprato.idcategoriaPrato
        WHERE prato.idPrato like %s
            OR prato.nome like %s
            OR prato.descricao LIKE %s
            Or categoriaprato.designacao LIKE %s
            """
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    if resultado == []:
        print(f"Nao foi encontrado o filtro `{filtro}´ nas pesquisas de pratos!")
    else:
        print(tabulate(resultado, headers=['IdPrato', 'NomeDoPrato', 'DescricaoDoPRATO', 'NomeCategoria'], tablefmt='psql'))

    '''if filtra_e_lista(cnx, data, sql) == 0:
        print(f'Nao encontrado o filtro {filtro}')'''
def main_le_opcao():
    print(80 * "#")
    print("""                Menu dos Pratos\n
                    1 - Veja todos os pratos disponiveis na Universidade
                    2 - Filtre o prato que deseja ver (Id, Nome, Descrição)
                    3 - Adicione um novo prato na base de dados
                    4 - Apague um prato da base de dados 
                    5 - Lista os pratos que já não se econtram disponivéis
                    6 - Lista dos pratos mais vendidos na Universidade desde sempre.
                    
                 v - Voltar Menu Anterior
                 x - sair
            """)
    print(80 * "#")
    op = input("opção? ")
    print(80 * "#")
    return op.upper()
def main_pratos():
    # try:
    cnx = mysql.connector.connect(**config)
    while True:
        op = main_le_opcao()
        if op == "1":  # lista todos os clientes
            lista_pratos(cnx)
        elif op == "2":  # lista clientes que satisfazem o filtro
            filtra_pratos(cnx)
        elif op == "3":  # insere um novo cliente
            insere_pratos(cnx)
        elif op == "4":
            apaga_prato(cnx)
        elif op == "5":
            mostra_pratos_nao_disponiveis(cnx)
        elif op == "6":
            lista_pratos_mais_vendidos(cnx)
        elif op == "x":
            exit()
        elif op == "V":
            print('Voltando...')
            break
    # except mysql.connector.Error as err:
    #     print('Ups! Ocorreu um erro!')
    #     print(err.errno)
    # else:
    cnx.close()