from utils import *
import mysql.connector
from config import config
from tabulate import tabulate


def lista_todas_as_avaliacoes(cnx):
    sql = """SELECT 
    cliente.cod_cliente,
    CONCAT(cliente.nome, ' ', cliente.apelido) AS nome,
    CONCAT(espacoalimentar.idespacoAlimentar,' - ',espacoalimentar.nome) AS EspAlim,
    nota,
    comentario
FROM
    barcantina.avaliacao
        INNER JOIN
    cliente ON cliente.cod_cliente = avaliacao.cod_cliente
        INNER JOIN
    espacoalimentar ON espacoalimentar.idespacoAlimentar = avaliacao.idespacoAlimentar

ORDER BY espacoalimentar.idespacoAlimentar , cod_cliente
"""
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['CodCliente', 'NomeCliente', 'EspacoAlimentar', 'Nota', 'Comentario'], tablefmt='psql'))

def lista_avaliacoes_de_um_espaco(cnx):
    sql = """SELECT 
        cliente.cod_cliente,
        CONCAT(cliente.nome, ' ', cliente.apelido) AS nome,
        CONCAT(espacoalimentar.idespacoAlimentar,' - ',espacoalimentar.nome) AS EspAlim,
        nota,
        comentario
    FROM
        barcantina.avaliacao
            INNER JOIN
        cliente ON cliente.cod_cliente = avaliacao.cod_cliente
            INNER JOIN
        espacoalimentar ON espacoalimentar.idespacoAlimentar = avaliacao.idespacoAlimentar

    WHERE espacoalimentar.idespacoAlimentar LIKE %s
    ORDER BY espacoalimentar.idespacoAlimentar , cod_cliente
    """
    filtro = input('Digite o Id do espaco alimentar que quer consultar as avaliações?')
    data = (filtro,)
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['CodCliente', 'NomeCliente', 'EspacoAlimentar', 'Nota', 'Comentario'],
                   tablefmt='psql'))

def lista_avaliacoes_de_um_cliente(cnx):
    sql = """SELECT 
            cliente.cod_cliente,
            CONCAT(cliente.nome, ' ', cliente.apelido) AS nome,
            CONCAT(espacoalimentar.idespacoAlimentar,' - ',espacoalimentar.nome) AS EspAlim,
            nota,
            comentario
        FROM
            barcantina.avaliacao
                INNER JOIN
            cliente ON cliente.cod_cliente = avaliacao.cod_cliente
                INNER JOIN
            espacoalimentar ON espacoalimentar.idespacoAlimentar = avaliacao.idespacoAlimentar

        WHERE cliente.cod_cliente LIKE %s
        ORDER BY espacoalimentar.idespacoAlimentar , cod_cliente
        """
    filtro = input('Digite o Id do cliente que quer consultar as avaliações?')
    data = (filtro,)
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['CodCliente', 'NomeCliente', 'EspacoAlimentar', 'Nota', 'Comentario'],
                   tablefmt='psql'))

def total_avaliacoes_clientes_por_espacoalimentar(cnx):
    sql = """SELECT 
        CONCAT(cliente.nome, ' ', cliente.apelido) AS nome,
        CONCAT(espacoalimentar.idespacoAlimentar,' - ',espacoalimentar.nome) AS EspAlim,
        count(nota) as avaliacoesfeitas
        
    FROM
        barcantina.avaliacao
            INNER JOIN
        cliente ON cliente.cod_cliente = avaliacao.cod_cliente
            INNER JOIN
        espacoalimentar ON espacoalimentar.idespacoAlimentar = avaliacao.idespacoAlimentar
  
  group by cliente.cod_cliente, espacoalimentar.idespacoAlimentar
    ORDER BY nome 
  
        """

    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['NomeCliente', 'EspacoAlimentar', 'TotalAvaliacoesFeitas'],
                   tablefmt='psql'))

def lista_media_avaliacao_cliente_especifico(cnx):
    sql = """ SELECT 
        cliente.cod_cliente,
        CONCAT(cliente.nome, ' ', cliente.apelido) AS nome,
        CONCAT(espacoalimentar.idespacoAlimentar,' - ',espacoalimentar.nome) AS EspAlim,
        Sum(nota)/count(avaliacao.cod_cliente)
    FROM
        barcantina.avaliacao
            INNER JOIN
        cliente ON cliente.cod_cliente = avaliacao.cod_cliente
            INNER JOIN
        espacoalimentar ON espacoalimentar.idespacoAlimentar = avaliacao.idespacoAlimentar
  WHERE avaliacao.cod_cliente LIKE %s
  group by espacoalimentar.idespacoAlimentar
    ORDER BY espacoalimentar.idespacoAlimentar 
   """
    filtro = input('Digite o Id do cliente que quer consultar a media de suas avaliações?')
    data = (filtro,)

    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['CodCliente', 'NomeCliente', 'EspacoAlimentar', 'MediaDeNota'],
                   tablefmt='psql'))

def lista_media_espaco_alimentar(cnx):
    sql = """ SELECT 
        CONCAT(espacoalimentar.idespacoAlimentar,' - ',espacoalimentar.nome) AS EspAlim,
        Sum(nota)/count(avaliacao.cod_cliente) as media
    FROM
        barcantina.avaliacao
            INNER JOIN
        cliente ON cliente.cod_cliente = avaliacao.cod_cliente
            INNER JOIN
        espacoalimentar ON espacoalimentar.idespacoAlimentar = avaliacao.idespacoAlimentar
  
  group by espacoalimentar.idespacoAlimentar
    ORDER BY espacoalimentar.idespacoAlimentar 
  """
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['EspacoAlimentar', 'Media'], tablefmt='psql'))

def total_de_avaliacoes_recebidas(cnx):
    sql = """ SELECT 
        CONCAT(espacoalimentar.idespacoAlimentar,' - ',espacoalimentar.nome) AS EspAlim,
        count(nota)
        
    FROM
        barcantina.avaliacao
            INNER JOIN
        cliente ON cliente.cod_cliente = avaliacao.cod_cliente
            INNER JOIN
        espacoalimentar ON espacoalimentar.idespacoAlimentar = avaliacao.idespacoAlimentar
  
  group by espacoalimentar.idespacoAlimentar
    ORDER BY espacoalimentar.idespacoAlimentar 
  
        """
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['EspacoAlimentar', 'TotalDeAvaliaçõesRecebidas'], tablefmt='psql'))

def inserir_avaliacao(cnx):
    sql = """ INSERT  INTO  avaliacao (
                        idavaliacao,
                        nota, 
                        comentario, 
                        cod_cliente,
                        idespacoAlimentar
                    ) VALUES (
                        DEFAULT, 
                        %(nota)s, 
                        %(comentario)s, 
                        %(cod_cliente)s,
                        %(idespacoAlimentar)s
                    )
            """
    print('Tenha Atenção ao colocar o cod_cliente\n Certifique-se que cliente está cadastrado')
    print('Tenha Atenção ao colocar o idespacoAlimentar\n Certifique-se que idespacoAlimentar existe')
    data = dict()
    for atributo in ("nota", "comentario", "cod_cliente","idespacoAlimentar"):
        data[atributo] = input(f"{atributo}? ")


    with cnx.cursor() as cursor:
        cursor.execute(sql, data)
        cnx.commit()
    print('Avaliação Adicionada')

def consultar_avaliacao_especifica(cnx):
    sql = '''SELECT 
    cliente.cod_cliente,
    CONCAT(cliente.nome, ' ', cliente.apelido) AS nome,
    CONCAT(espacoalimentar.idespacoAlimentar,' - ',espacoalimentar.nome) AS EspAlim,
    nota,
    comentario
FROM
    barcantina.avaliacao
        INNER JOIN
    cliente ON cliente.cod_cliente = avaliacao.cod_cliente
        INNER JOIN
    espacoalimentar ON espacoalimentar.idespacoAlimentar = avaliacao.idespacoAlimentar
WHERE idavaliacao LIKE %s
ORDER BY espacoalimentar.idespacoAlimentar , cod_cliente'''
    filtro = input("Qual id avalicao quer consultar?")
    data = (filtro,)
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['CodCliente', 'NomeCliente', 'EspacoAlimentar', 'Nota', 'Comentario'],
                   tablefmt='psql'))


def main_le_opcao():
    print(80 * "#")
    print("""                Menu Avaliação dos Espaços Alimentares\n
                    1 - Veja todos os registos de avaliacoes feitas.
                    2 - Filtre por espaco alimentar as avaliacoes.
                    3 - Filtre por cliente as avaliacoes.
                    4 - Liste quantas avaliacoes foram feitas pelos clientes no espaco alimentar especifico
                    5 - Lista a media dos espacos alimentares por cliente.
                    6 - Lista a media global da avaliaçao daquele espaço.
                    7 - Lista o total de avaliações que cada espaco recebeu.
                    8 - Insira uma nova avaliação
                    9 - Consulte uma avaliação especifica pelo seu id

                 v - Voltar Menu Anterior
                 x - sair
            """)
    print(80 * "#")
    op = input("opção? ")
    print(80 * "#")
    return op


def main_avaliacao():
    # try:
    cnx = mysql.connector.connect(**config)
    while True:
        op = main_le_opcao()
        if op == "1":
            lista_todas_as_avaliacoes(cnx)
        elif op == "2":
            lista_avaliacoes_de_um_espaco(cnx)
        elif op == "3":
            lista_avaliacoes_de_um_cliente(cnx)
        elif op == "4":
            total_avaliacoes_clientes_por_espacoalimentar(cnx)
        elif op == "5":
            lista_media_avaliacao_cliente_especifico(cnx)
        elif op == "6":
            lista_media_espaco_alimentar(cnx)
        elif op == "7":
            total_de_avaliacoes_recebidas(cnx)
        elif op == "8":
            inserir_avaliacao(cnx)
        elif op == "9":
            consultar_avaliacao_especifica(cnx)
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