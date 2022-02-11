from utils import *


# def filtra_cliente(cnx):
#     filtro = input("Filtro (e.g., %Po%) ?")
#     data = 5 * (filtro,)
#     sql = """ SELECT *
#         FROM clientes
#         WHERE NomeDaEmpresa like %s
#             OR NomeDoContacto like %s
#             OR CargoDoContacto LIKE %s
#             OR Cidade LIKE %s
#             OR País LIKE %s
#             """
#     # print(sql)
#     filtra_e_lista(cnx, data, sql)


def lista_instituto(cnx):
    sql = """ SELECT * FROM Instituto """
    data = None
    filtra_e_lista(cnx, data, sql)

def filtra_istitutos(cnx):
    filtro = input("filtro ?")
    data = 1 * (filtro,)
    sql = """ SELECT * 
            FROM instituto 
            WHERE designacao like %s 
                """
    # print(sql)
    filtra_e_lista(cnx, data, sql)

def filtra_espaco(cnx):
    filtro = input("Filtro (e.g., %Po%) ?")
    data = 1 * (filtro,)
    sql = """SELECT CONCAT(espacoalimentar.idespacoAlimentar , ' - ' , instituto.designacao ) as instituto, 
espacoalimentar.idespacoAlimentar,
espacoalimentar.nome, espacoalimentar.idinstituto
FROM espacoalimentar
inner join instituto
on espacoalimentar.idinstituto = instituto.idinstituto
    WHERE nome like %s
                """
    # print(sql)
    filtra_e_lista(cnx, data, sql)

def filtra_cliente(cnx):
    filtro = input("Filtro (e.g., %Po%) ?")
    data = 3 * (filtro,)
    sql= """SELECT * FROM cliente
    WHERE numero_telefone like %s
    or nome like %s
    or apelido like %s
    """

    #print (sql)
    filtra_e_lista(cnx,data,sql)

def filtra_fornecedor(cnx):
    filtro=input("Filtro (e.g., %Po%) ?")
    data= 1 * (filtro,)
    sql="""SELECT * FROM fornecedor
    WHERE nome like %s"""

    filtra_e_lista(cnx,data,sql)


def espaço_alimentar(cnx):
    sql= """SELECT * FROM espacoalimentar """
    data= None
    filtra_e_lista(cnx,data,sql)

# def fornecedores(cnx):
#     sql= """"SELECT * FROM fornecedores"""
#     data= None
#     filtra_e_lista(cnx,data,sql)

def cliente(cnx):
    sql="""SELECT * FROM cliente"""
    data= None
    filtra_e_lista(cnx,data,sql)






def insere_cliente(cnx):
    sql = """ INSERT  INTO  cliente (
                    CódigoDoCliente, 
                    NomeDaEmpresa, 
                    NomeDoContacto, 
                    CargoDoContacto, 
                    Endereço, 
                    Cidade, 
                    Região, 
                    CódigoPostal, 
                    País, 
                    Telefone, 
                    Fax
                ) VALUES (
                    DEFAULT, 
                    %(NomeDaEmpresa)s, 
                    %(NomeDoContacto)s, 
                    %(CargoDoContacto)s,
                    %(Endereço)s,
                    %(Cidade)s, 
                    %(Região)s, 
                    %(CódigoPostal)s, 
                    %(País)s, 
                    %(Telefone)s, 
                    %(Fax)s
                )
        """
    data = dict()
    for atributo in ("NomeDaEmpresa", "NomeDoContacto", "CargoDoContacto", "Endereço", "Cidade",
                     "Região", "CódigoPostal", "País", "Telefone", "Fax"):
        data[atributo] = input(f"{atributo}? ")

    with cnx.cursor() as cursor:
        cursor.execute(sql, data)
        cnx.commit() 


