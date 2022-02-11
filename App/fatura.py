from utils import *
from datetime import datetime
import mysql.connector
from precoPratoEspacoAlimentar import *
from precoProdutoEspacoAlimentar import *
from config import config
from tabulate import tabulate


def lista_faturas(cnx):
    sql = """ SELECT *
FROM ((SELECT fatura.idfatura as numfatura, fatura.data, espacoalimentar.nome, funcionario.nome as nomeFuncionario,  cliente.nome as nomeCliente
FROM fatura
INNER JOIN funcionario ON fatura.idfuncionario = funcionario.idfuncionario
INNER JOIN espacoalimentar ON funcionario.idespacoAlimentar = espacoalimentar.idespacoAlimentar
INNER JOIN produtoespacoalimentar ON produtoespacoalimentar.idespacoAlimentar = espacoalimentar.idespacoAlimentar
INNER JOIN pratofatura ON pratofatura.idfatura = fatura.idfatura
INNER JOIN prato ON pratofatura.idprato = prato.idprato
INNER JOIN pratoespacoalimentar ON pratoespacoalimentar.idprato = prato.idprato
INNER JOIN instituto ON espacoalimentar.idinstituto = instituto.idinstituto
INNER JOIN cliente ON fatura.cod_cliente = cliente.cod_cliente
Group By numfatura
)
UNION
(SELECT fatura.idfatura as numfatura, fatura.data, espacoalimentar.nome,
 funcionario.nome as nomeFuncionario, cliente.nome as nomeCliente
FROM fatura
INNER JOIN funcionario ON fatura.idfuncionario = funcionario.idfuncionario
INNER JOIN espacoalimentar ON funcionario.idespacoAlimentar = espacoalimentar.idespacoAlimentar
INNER JOIN produtoespacoalimentar ON produtoespacoalimentar.idespacoAlimentar = espacoalimentar.idespacoAlimentar
INNER JOIN produtofatura ON produtofatura.idfatura = fatura.idfatura
INNER JOIN produto ON produtoespacoalimentar.idproduto = produto.idproduto
INNER JOIN instituto ON espacoalimentar.idinstituto = instituto.idinstituto
INNER JOIN cliente ON fatura.cod_cliente = cliente.cod_cliente
Group By numfatura

)) AS faturaGlobal
ORDER BY numfatura  """
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['NumFatura', 'Data', 'EspacoAlimentar', 'Funcionario', 'Cliente'], tablefmt='psql'))

def lista_faturas_plus(cnx):
    lista_faturas(cnx)

    print(80 * "#")
    print("""                Menu Pratos\n
                    1 - Visualizar Detalhes de uma fatura especifica
                    2 - Voltar ao menu das faturas

            """)
    print(80 * "#")
    op = input("opção? ")
    print(80 * "#")

    if op == "1":
        lista_detalhes_faturas(cnx)
    elif op == "2":
        pass


def delete_faturas(cnx):
    lista_faturas(cnx)
    filtro = input("Qual o id da fatura que deseja apagar? ")
    data = (filtro,)
    sql = """Delete from fatura where idfatura like %s"""
    with cnx.cursor() as cursor:
        cursor.execute(sql,data)
        cnx.commit()
    print("Fatura apagada")
def lista_detalhes_faturas(cnx):

    sqlDados = """ SELECT * 
        FROM ((SELECT fatura.idfatura as numfatura, fatura.data, espacoalimentar.nome as espacoAlimentar,
         funcionario.nome as nomeFuncionario,  cliente.nome as nomeCliente
        FROM fatura 
        INNER JOIN funcionario ON fatura.idfuncionario = funcionario.idfuncionario
        INNER JOIN espacoalimentar ON funcionario.idespacoAlimentar = espacoalimentar.idespacoAlimentar
        INNER JOIN produtoespacoalimentar ON produtoespacoalimentar.idespacoAlimentar = espacoalimentar.idespacoAlimentar
        INNER JOIN pratofatura ON pratofatura.idfatura = fatura.idfatura
        INNER JOIN prato ON pratofatura.idprato = prato.idprato
        INNER JOIN pratoespacoalimentar ON pratoespacoalimentar.idprato = prato.idprato
        INNER JOIN instituto ON espacoalimentar.idinstituto = instituto.idinstituto
        INNER JOIN cliente ON fatura.cod_cliente = cliente.cod_cliente
        )
        UNION
        (SELECT fatura.idfatura as numfatura, fatura.data, espacoalimentar.nome,
         funcionario.nome as nomeFuncionario, cliente.nome as nomeCliente
        FROM fatura 
        INNER JOIN funcionario ON fatura.idfuncionario = funcionario.idfuncionario
        INNER JOIN espacoalimentar ON funcionario.idespacoAlimentar = espacoalimentar.idespacoAlimentar
        INNER JOIN produtoespacoalimentar ON produtoespacoalimentar.idespacoAlimentar = espacoalimentar.idespacoAlimentar
        INNER JOIN produtofatura ON produtofatura.idfatura = fatura.idfatura
        INNER JOIN produto ON produtoespacoalimentar.idproduto = produto.idproduto
        INNER JOIN instituto ON espacoalimentar.idinstituto = instituto.idinstituto
        INNER JOIN cliente ON fatura.cod_cliente = cliente.cod_cliente
        )) AS faturaGlobal
        WHERE numfatura = %(numFatura)s
         """
    sqlItens = """ SELECT 
    *
    FROM
    ((SELECT 
        produtofatura.idfatura AS idf,
        produtofatura.idproduto AS id_item,
        produto.designacao AS Item,
        produtofatura.quantidade AS qtd,
        produtoespacoalimentar.preco AS preco,
        (produtoespacoalimentar.preco *  produtofatura.quantidade) as subtotal
    FROM
        produtofatura
    INNER JOIN produtoespacoalimentar ON produtofatura.idproduto = produtoespacoalimentar.idproduto INNER JOIN produto ON produtoespacoalimentar.idproduto = produto.idproduto
        AND produtofatura.idespacoAlimentar = produtoespacoalimentar.idespacoAlimentar
    INNER JOIN fatura ON fatura.idfatura = produtofatura.idfatura) UNION (SELECT 
        pratofatura.idfatura AS idf,
        pratofatura.idprato AS id_item,
        prato.nome AS Item,
        pratofatura.quantidade AS qtd,
        pratoespacoalimentar.preco AS preco,
        (pratoespacoalimentar.preco * pratofatura.quantidade) as subtotal
    FROM
        pratofatura
        INNER JOIN pratoespacoalimentar ON pratofatura.idprato = pratoespacoalimentar.idprato INNER JOIN prato ON pratoespacoalimentar.idprato = prato.idprato
        AND pratofatura.idespacoAlimentar = pratoespacoalimentar.idespacoAlimentar
        INNER JOIN fatura ON fatura.idfatura = pratofatura.idfatura)
        ) AS faturaglobal
        where idf = %(numFatura)s
        ORDER BY idf
                """
    sqlTotal ="""
    SELECT 
    SUM(subtotal)
    FROM
    ((SELECT 
        produtofatura.idfatura AS idf,
        fatura.data AS data,
        espacoalimentar.nome AS espacoAlim,
        produtofatura.idproduto AS id_item,
        produto.designacao AS Item,
        produtofatura.quantidade AS qtd,
        produtoespacoalimentar.preco AS preco,
        (produtoespacoalimentar.preco *  produtofatura.quantidade) as subtotal
            
    FROM espacoalimentar INNER JOIN produtofatura ON espacoalimentar.idespacoalimentar = produtofatura.idespacoAlimentar
    INNER JOIN produtoespacoalimentar ON produtofatura.idproduto = produtoespacoalimentar.idproduto INNER JOIN produto ON produtoespacoalimentar.idproduto = produto.idproduto
        AND produtofatura.idespacoAlimentar = produtoespacoalimentar.idespacoAlimentar
    INNER JOIN fatura ON fatura.idfatura = produtofatura.idfatura) UNION (SELECT 
        pratofatura.idfatura AS idf,
        fatura.data AS data,
        espacoalimentar.nome AS espacoAlim,
        pratofatura.idprato AS id_item,
        prato.nome AS Item,
        pratofatura.quantidade AS qtd,
        pratoespacoalimentar.preco AS preco,
        (pratoespacoalimentar.preco * pratofatura.quantidade) as subtotal
    FROM
       espacoalimentar INNER JOIN pratofatura ON espacoalimentar.idespacoalimentar = pratofatura.idespacoAlimentar
    INNER JOIN pratoespacoalimentar ON pratofatura.idprato = pratoespacoalimentar.idprato INNER JOIN prato ON pratoespacoalimentar.idprato = prato.idprato
        AND pratofatura.idespacoAlimentar = pratoespacoalimentar.idespacoAlimentar
    INNER JOIN fatura ON fatura.idfatura = pratofatura.idfatura)
    ) AS faturaglobal
    WHERE idf = %(numFatura)s
    ORDER BY idf
    """

    filtro = int(input('numFatura?'))
    data = {'numFatura':filtro}

    cursor = cnx.cursor()
    cursor.execute(sqlDados, data)


    resultadoDados = cursor.fetchall()
    print("Dados da Fatura")
    print(tabulate(resultadoDados, headers=['NumFatura', 'Data', 'EspacoAlimentar', 'Funcionario', 'Cliente        '], tablefmt='psql'))

    cursor = cnx.cursor()
    cursor.execute(sqlItens, data)

    resultadoItens= cursor.fetchall()
    print("Produtos")
    print(tabulate(resultadoItens, headers=['NumFatura', 'IDProduto', 'Produto', 'Quantidade', 'Preco-Un/€', 'SubTotal/€ ', 'Total/€'], tablefmt='psql'))

    cursor = cnx.cursor()
    cursor.execute(sqlTotal, data)

    resultadoTotal= cursor.fetchall()
    print(tabulate(resultadoTotal, headers=['Total/€'], tablefmt='psql'))



def insere_faturas(cnx):

    sqlInstituto = """SELECT idespacoAlimentar, nome FROM espacoalimentar"""
    data = None
    cursor = cnx.cursor()
    cursor.execute(sqlInstituto, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['ID', 'EspacoAlimentar'], tablefmt='psql'))

    data = dict()
    for atributo in ("idfuncionario", "data", "cod_cliente"):
        if(atributo == "cod_cliente"):
            data[atributo] = input(f"{atributo}? ")
        elif(atributo == "idfuncionario"):

            sql1 = """SELECT idfuncionario, CONCAT(funcionario.nome, " ", funcionario.apelido ) as nome 
            FROM barcantina.funcionario 
            WHERE idespacoAlimentar LIKE %s
            """
            filtro1 = input("idespacoAlimentar: ")
            data1 = (filtro1,)

            cursor1 = cnx.cursor()
            cursor1.execute(sql1, data1)
            resultado1 = cursor1.fetchall()

            print(tabulate(resultado1, headers=['idFuncionario', 'nome'], tablefmt='psql'))
            print("!!!!ATENÇÃO!!!")
            print("Preencha o campo idfuncionario com um id já existente, pode verificar os id´s na tabela acima")
            data[atributo] = input(f"{atributo}? ")

        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        data['data'] = f"{dt_string}"

    sql = """ INSERT  INTO  fatura (
                        idfatura,
                        idfuncionario, 
                        data,
                        cod_cliente

                    ) VALUES (
                        DEFAULT,
                        %(idfuncionario)s,
                        %(data)s, 
                        %(cod_cliente)s
                    )
            """

    with cnx.cursor() as cursor2:
        cursor2.execute(sql, data)
        cnx.commit()
        idf = cursor2.lastrowid
    inserir_itens(cnx, idf, filtro1)

def verificar_stock_produto(cnx,idproduto, idespacoAlimentar, quantidade):
    sql = """SELECT stock FROM produtoespacoalimentar where idproduto = %(idproduto)s and idespacoAlimentar = %(idespacoAlimentar)s"""
    data = {'idproduto': idproduto, 'idespacoAlimentar' : idespacoAlimentar}
    cursor = cnx.cursor()
    cursor.execute(sql, data)

    resultado = cursor.fetchall()

    stock = resultado[0][0]

    stock2 = int(stock) - int(quantidade)

    if(stock2 <= 0):
        return 0
    else:
        return 1
def retirar_stock_produto(cnx, idproduto, idespacoAlimentar, quantidade):
    sql1 = """SELECT stock FROM produtoespacoalimentar where idproduto = %(idproduto)s and idespacoAlimentar = %(idespacoAlimentar)s"""
    data1 = {'idproduto': idproduto, 'idespacoAlimentar' : idespacoAlimentar}
    cursor = cnx.cursor()
    cursor.execute(sql1, data1)

    resultado = cursor.fetchall()

    stock = resultado[0][0]
    stockNovo = int(stock) - int(quantidade)

    sql = """Update produtoespacoalimentar SET stock = %(stock)s where idproduto = %(idproduto)s and idespacoAlimentar = %(idespacoAlimentar)s"""
    data = {'stock': stockNovo, 'idproduto': idproduto, 'idespacoAlimentar': idespacoAlimentar}
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    cnx.commit()

def inserir_itens(cnx, idf, idea):
    continuarEncomenda = True
    while continuarEncomenda:
        print("="*20)
        print("1-Introduzir um produto")
        print("2-Introduzir um prato")
        print("3-Finalizar pedido")
        op = input("Opção: ")
        print("="*20)

        if(op == "1"):
            lista_preco_produto_espacoalimentar_especifico_2(cnx, idea)
            sql = """ INSERT  INTO  produtofatura (
                                idproduto,
                                idfatura, 
                                quantidade,
                                idespacoAlimentar

                            ) VALUES (
                                %(idproduto)s,
                                %(idfatura)s,
                                %(quantidade)s, 
                                %(idespacoAlimentar)s
                            )
                    """
            data = dict()
            for atributo in ("idproduto", "quantidade"):
                if (atributo == "idproduto"):
                    data[atributo] = input(f"{atributo}? ")
                    idproduto = data['idproduto']
                elif(atributo == "quantidade"):
                    data[atributo] = input(f"{atributo}? ")
                    quantidade = data['quantidade']
            data["idespacoAlimentar"] = idea
            data["idfatura"] = idf
            cursor = cnx.cursor()
            if(verificar_stock_produto(cnx,idproduto,idea,quantidade) == 1):
                retirar_stock_produto(cnx,idproduto,idea,quantidade)
                cursor.execute(sql, data)
                cnx.commit()
            else:
                print("Quantidade inexistente")

        elif(op == "2"):
            lista_preco_prato_espacoalimentar_especifico_2(cnx,idea)
            sql = """ INSERT  INTO  pratofatura (
                                            idfatura,
                                            idprato,
                                            quantidade,
                                            idespacoAlimentar

                                        ) VALUES (
                                            %(idfatura)s,
                                            %(idprato)s,
                                            %(quantidade)s, 
                                            %(idespacoAlimentar)s
                                        )
                                """
            data = dict()
            for atributo in ("idprato", "quantidade"):
                if (atributo == "idprato"):
                    data[atributo] = input(f"{atributo}? ")
                elif (atributo == "quantidade"):
                    data[atributo] = input(f"{atributo}? ")
            data["idespacoAlimentar"] = idea
            data["idfatura"] = idf
            cursor = cnx.cursor()
            cursor.execute(sql, data)
            cnx.commit()
        elif(op == "3"):
            continuarEncomenda = False



def main_le_opcao():
    print(80 * "#")
    print("""                Menu Faturas\n
                    1 - Visualizar todas as faturas
                    2 - Adicione uma nova fatura na base de dados
                    3 - Apague uma fatura da base de dados 
                 
                 v - Voltar Menu Anterior
                 x - sair
            """)
    print(80 * "#")
    op = input("opção? ")
    print(80 * "#")
    return op

def main_fatura():
    # try:
    cnx = mysql.connector.connect(**config)
    while True:
        op = main_le_opcao()
        if op == "1":  # lista todas as faturas
            lista_faturas_plus(cnx)
        elif op == "2":  # adiciona fatura
            insere_faturas(cnx)
        elif op == "3":  # apaga fatura
            delete_faturas(cnx)
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

