from pprint import pprint


def filtra_e_lista(cnx, data, sql):
    i = -1
    with cnx.cursor(dictionary=True) as cursor:
        cursor.execute(sql, data)
        for i, row in enumerate(cursor):
            pprint( row)

    return i + 1

        # listar todos de uma vez:
        # cursor.execute(sql, data)
        # pprint(cursor.fetchall())



