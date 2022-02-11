from utils import *
import mysql.connector
from config import config
from tabulate import tabulate

def lista_funcionarios(cnx):
    sql = """ SELECT funcionario.idfuncionario, funcionario.nome, funcionario.apelido, espacoalimentar.nome
        FROM funcionario INNER JOIN espacoAlimentar
        ON funcionario.idEspacoAlimentar = espacoAlimentar.idEspacoAlimentar
         ORDER BY funcionario.idfuncionario"""
    data = None
    cursor = cnx.cursor()
    cursor.execute(sql, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['IDFuncionário', 'Nome', 'Apelido', 'EspacoAlimentar'],
                   tablefmt='psql'))




def insere_funcionario(cnx):
    sqlInstituto = """SELECT idespacoAlimentar, nome FROM barcantina.espacoalimentar"""
    data = None
    cursor = cnx.cursor()
    cursor.execute(sqlInstituto, data)
    resultado = cursor.fetchall()
    print(tabulate(resultado, headers=['ID', 'EspacoAlimentar'], tablefmt='psql'))
    print("!!!!ATENÇÃO!!!")
    print("Preencha o campo idEspacoAlimentar com um id já existente, pode verificar os id´s na tabela acima")
    sql = """ INSERT  INTO  funcionario (
                    nome,
                    apelido,
                    idEspacoAlimentar

                ) VALUES ( 
                    %(nome)s,
                    %(apelido)s,  
                    %(idEspacoAlimentar)s
                )
        """
    data = dict()
    for atributo in ("nome", "apelido", "idEspacoAlimentar"):
        data[atributo] = input(f"{atributo}? ")

    with cnx.cursor() as cursor:
        cursor.execute(sql, data)
        cnx.commit()

def edita_funcionario(cnx):
    i = 1
    while i > 0:
        if(i > 1):
            print("Funcionário editado com sucesso!!!")
            op = input("Pretende Fazer mais alguma alteração?(s/n)")
            if(op.lower() == "s"):
                pass
            else:
                break
        i = i+1
        print("="*20)
        print("Modificar dados de um funcionário")
        print("="*20)
        lista_funcionarios(cnx)
        idFuncionario = int(input("Introduza o id do funcionario que pertende modificar: "))
        print("="*20)
        print("Opções de modificação")
        print("="*20)
        print("1-Nome")
        print("2-Apelido")
        print("3-Espaco Alimentar")
        campo = int(input("Opção: "))
        if(campo == 1):
            edita_nome(cnx, idFuncionario)
        if (campo == 2):
            edita_apelido(cnx, idFuncionario)
        if (campo == 3):
            edita_espacoAlimentar(cnx, idFuncionario)
        else:
            pass

def edita_nome(cnx,idFuncionario):
    sqlCampo = """SELECT nome FROM funcionario Where idfuncionario = %(idfuncionario)s"""

    filtro = idFuncionario
    data = {'idfuncionario':filtro}

    cursor = cnx.cursor()
    cursor.execute(sqlCampo, data)
    resultado = cursor.fetchall()
    print("="* 20)
    print("Nome Antigo")
    print(tabulate(resultado, headers=['Nome'], tablefmt='psql'))
    sql2 = """ UPDATE funcionario SET nome = %(nome)s Where funcionario.idfuncionario = %(idfuncionario)s"""
    data2 = dict()
    data2['nome'] = input("Novo Nome? ")
    data2['idfuncionario'] = idFuncionario

    with cnx.cursor() as cursor:
        cursor.execute(sql2, data2)
        cnx.commit()

def edita_apelido(cnx,idFuncionario):
    sqlCampo = """SELECT apelido FROM funcionario Where idfuncionario = %(idfuncionario)s"""
    filtro = idFuncionario
    data = {'idfuncionario':filtro}

    cursor = cnx.cursor()
    cursor.execute(sqlCampo, data)
    resultado = cursor.fetchall()
    print("="* 20)
    print("Apelido Antigo")
    print(tabulate(resultado, headers=['Apelido'], tablefmt='psql'))
    sql2 = """ UPDATE funcionario SET apelido = %(apelido)s Where funcionario.idfuncionario = %(idfuncionario)s"""
    data2 = dict()
    data2['apelido'] = input("Novo Apelido? ")
    data2['idfuncionario'] = idFuncionario

    with cnx.cursor() as cursor:
        cursor.execute(sql2, data2)
        cnx.commit()

def edita_espacoAlimentar(cnx,idFuncionario):
    sqlCampo = """SELECT funcionario.idespacoAlimentar, espacoalimentar.nome FROM funcionario 
    INNER JOIN espacoalimentar ON  funcionario.idespacoAlimentar = espacoalimentar.idespacoAlimentar
    Where idfuncionario = %(idfuncionario)s"""
    filtro = idFuncionario
    data = {'idfuncionario':filtro}

    cursor = cnx.cursor()
    cursor.execute(sqlCampo, data)
    resultado = cursor.fetchall()
    print("="* 20)
    print("Espaco Alimentar Antigo")
    print(tabulate(resultado, headers=['IdEspacoAlimentar'], tablefmt='psql'))
    print("="* 20)

    sql3 = """SELECT idespacoAlimentar, nome from espacoalimentar"""
    data3 = None
    cursor3 = cnx.cursor()
    cursor3.execute(sql3, data3)
    resultado3 = cursor3.fetchall()
    print("="* 20)
    print("Espaco Alimentar Antigo")
    print(tabulate(resultado3, headers=['IdEspacoAlimentar', 'Nome'], tablefmt='psql'))
    print("="* 20)
    sql2 = """ UPDATE funcionario SET idespacoAlimentar = %(idespacoAlimentar)s 
                Where idfuncionario = %(idfuncionario)s"""
    data2 = dict()
    data2['idespacoAlimentar'] = input("IdEspacoAlimentar novo? ")
    data2['idfuncionario'] = idFuncionario

    with cnx.cursor() as cursor:
        cursor.execute(sql2, data2)
        cnx.commit()

# def elimina_funcionario(cnx):
#     sqlInstituto = """SELECT idfuncionario, funcionario.nome, apelido, espacoalimentar.nome
#     FROM barcantina.funcionario INNER JOIN espacoalimentar
#     ON funcionario.idespacoAlimentar = espacoalimentar.idespacoAlimentar ORDER BY idfuncionario
#     """
#     cursor = cnx.cursor()
#     cursor.execute(sqlInstituto)
#     resultado = cursor.fetchall()
#     print(tabulate(resultado, headers=['ID', 'Nome', 'Apelido', 'EspacoAlimentar'], tablefmt='psql'))
#
#     sql = """ delete from funcionario where idfuncionario = %(idfuncionario)s """
#     print("!!!!ATENÇÃO!!!")
#     print("Preencha o campo idFuncionário com um id já existente, pode verificar os id´s na tabela acima")
#
#     data = dict()
#     filtro = int(input('idfuncionario?'))
#     data = {'idfuncionario':filtro}
#
#     with cnx.cursor() as cursor:
#         cursor.execute(sql, data)
#         cnx.commit()



def main_le_opcao():
    print(80 * "#")
    print("""                Menu Funcionarios\n
                    1 - Visualizar todos os Funcionários
                    2 - Adicione um novo funcionario na base de dados
                    3 - Editar um funcionário

                 v - Voltar Menu Anterior
                 x - sair
            """)
    print(80 * "#")
    op = input("opção? ")
    print(80 * "#")
    return op

def main_funcionarios():

    cnx = mysql.connector.connect(**config)
    while True:
        op = main_le_opcao()
        if op == "1":  # lista todas as faturas
            lista_funcionarios(cnx)
        elif op == "2":  # lista clientes que satisfazem o filtro
            insere_funcionario(cnx)
            print("Funcionário adicionado com sucesso!!!")
        elif op == "3":  # lista clientes que satisfazem o filtro
            edita_funcionario(cnx)
        elif op == "v":
            break
        elif op == "x":
            exit()
        # elif op == "4":
        #     elimina_funcionario(cnx)
        #     print('Apagado')


   

