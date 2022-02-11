from utils import *
import mysql.connector
from config import config
from tabulate import tabulate

def lista_melhor_funcionarios(cnx):
    sql11 = """SELECT fatura.idfuncionario, concat(funcionario.nome, " ",funcionario.apelido) as nome, count(fatura.idfuncionario) as numVendas FROM barcantinas.fatura
            INNER JOIN funcionario ON fatura.idfuncionario = funcionario.idfuncionario
            group by fatura.idfuncionario 
            order by idfuncionario asc"""
    sql12 = """SELECT fatura.idfuncionario, concat(funcionario.nome, " ",funcionario.apelido) as nome, count(fatura.idfuncionario) as numVendas FROM barcantinas.fatura
            INNER JOIN funcionario ON fatura.idfuncionario = funcionario.idfuncionario
            group by fatura.idfuncionario 
            order by idfuncionario desc"""

    sql21 = """SELECT fatura.idfuncionario, concat(funcionario.nome, " ",funcionario.apelido) as nome, count(fatura.idfuncionario) as numVendas FROM barcantinas.fatura
            INNER JOIN funcionario ON fatura.idfuncionario = funcionario.idfuncionario
            group by fatura.idfuncionario 
            order by nome asc"""
    sql22 = """SELECT fatura.idfuncionario, concat(funcionario.nome, " ",funcionario.apelido) as nome, count(fatura.idfuncionario) as numVendas FROM barcantinas.fatura
            INNER JOIN funcionario ON fatura.idfuncionario = funcionario.idfuncionario
            group by fatura.idfuncionario 
            order by nome desc"""

    sql31 = """SELECT fatura.idfuncionario, concat(funcionario.nome, " ",funcionario.apelido) as nome, count(fatura.idfuncionario) as numVendas FROM barcantinas.fatura
            INNER JOIN funcionario ON fatura.idfuncionario = funcionario.idfuncionario
            group by fatura.idfuncionario 
            order by numVendas asc"""
    sql32 = """SELECT fatura.idfuncionario, concat(funcionario.nome, " ",funcionario.apelido) as nome, count(fatura.idfuncionario) as numVendas FROM barcantinas.fatura
            INNER JOIN funcionario ON fatura.idfuncionario = funcionario.idfuncionario
            group by fatura.idfuncionario 
            order by numVendas desc"""

    print("="*20)
    print("Ordenar")
    print("1-Ordenar por idFuncionario")
    print("2-Ordenar pelo nome do funcionário")
    print("3-Ordenar pelo numero de vendas")
    campo = int(input('Opção?'))
    print("1-Ordenar por ordem ascendente")
    print("2-Ordenar por ordem descendente")
    ordem = int(input('Opção?'))
    print("="*20)

    data = None
    cursor = cnx.cursor()
    if(campo == 1 and ordem == 1):
        cursor.execute(sql11, data)
    elif(campo == 1 and ordem == 2):
        cursor.execute(sql12, data)
    elif(campo == 2 and ordem == 1):
        cursor.execute(sql21, data)
    elif(campo == 2 and ordem == 2):
        cursor.execute(sql22, data)
    elif(campo == 3 and ordem == 1):
        cursor.execute(sql31, data)
    elif(campo == 3 and ordem == 2):
        cursor.execute(sql32, data)

    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IDFuncionário', 'Nome', 'Numero de Vendas'],tablefmt='psql'))

def lista_espacoAlimentar(cnx):
    sqlInstituto = """SELECT idespacoAlimentar, nome FROM barcantinas.espacoalimentar"""
    data = None
    cursor = cnx.cursor()
    cursor.execute(sqlInstituto, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['ID', 'EspacoAlimentar'], tablefmt='psql'))


def lista_num_pratos(cnx):
    sql11 = """SELECT pratofatura.idprato, nome, count(pratofatura.idprato) as numPrato FROM pratofatura 
            INNER JOIN prato ON pratofatura.idprato = prato.idprato WHERE idespacoAlimentar = %s  group by pratofatura.idprato order by numPrato asc"""

    sql12 = """SELECT pratofatura.idprato, nome, count(pratofatura.idprato) as numPrato FROM pratofatura 
            INNER JOIN prato ON pratofatura.idprato = prato.idprato WHERE idespacoAlimentar = %s  group by pratofatura.idprato order by numPrato desc"""

    sql21 = """SELECT pratofatura.idprato, nome, count(pratofatura.idprato) as numPrato FROM pratofatura 
            INNER JOIN prato ON pratofatura.idprato = prato.idprato WHERE idespacoAlimentar = %s  group by pratofatura.idprato order by pratofatura.idprato asc"""

    sql22 = f"""SELECT pratofatura.idprato, nome, count(pratofatura.idprato) as numPrato FROM pratofatura 
            INNER JOIN prato ON pratofatura.idprato = prato.idprato WHERE idespacoAlimentar = %s  group by pratofatura.idprato order by pratofatura.idprato desc"""

    print("="*20)
    lista_espacoAlimentar(cnx)
    print("="*20)
    filtro = int(input("Introduza o id do espaço alimentar: "))
    print("="*20)
    print("Ordenar")
    print("1-Ordenar pelo numero de pratos vendidos")
    print("2-Ordenar por idPrato")
    campo = int(input('Opção?'))
    print("1-Ordenar por ordem ascendente")
    print("2-Ordenar por ordem descendente")
    ordem = int(input('Opção?'))
    print("="*20)

    data = (filtro,)

    cursor = cnx.cursor()
    if(campo == 1 and ordem == 1):
        cursor.execute(sql11, data)
    elif(campo == 1 and ordem == 2):
        cursor.execute(sql12, data)
    elif(campo == 2 and ordem == 1):
        cursor.execute(sql21, data)
    elif(campo == 2 and ordem == 2):
        cursor.execute(sql22, data)

    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IdPrato', 'Designacao', 'Numero de Vendas'], tablefmt='psql'))

def main_le_opcao():
    print(80 * "#")
    print("""                Menu Estatisticas\n
                    1 - Visualizar o numero de vendas de cada funcionário
                    2 - Visualizar o numero de pratos vendidos em cada espaço Alimentar

            """)
    print(80 * "#")
    op = input("opção? ")
    print(80 * "#")
    return op

def main_estatisticas():
    # try:
    cnx = mysql.connector.connect(**config)
    while True:
        op = main_le_opcao()
        if op == "1":  # lista todas as faturas
            lista_melhor_funcionarios(cnx)
        if op == "2":  # lista todas os pratos
            lista_num_pratos(cnx)

    cnx.close()

main_estatisticas()