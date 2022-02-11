from pprint import pprint


def filtra_e_lista(cnx, data, sql):
    with cnx.cursor(dictionary=True) as cursor:
        cursor.execute(sql, data)
        for row in cursor:
            pprint(row)

        # listar todos de uma vez:
        # cursor.execute(sql, data)
        # pprint(cursor.fetchall())



