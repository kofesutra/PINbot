import psycopg

from Config.config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE, DB_TABLE


# def is_in_base(request):
#     connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
#     connection.autocommit = True
#
#     with connection.cursor() as cursor:
#         cursor.execute(f"SELECT {request} FROM {DB_TABLE}")
#         return cursor.fetchall()


def add_all_to_db(columns_here, data_here):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO {DB_TABLE} ({columns_here}) VALUES ({data_here})")


def update_email_db(value, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE {DB_TABLE} SET email = '{value}' WHERE id = {condition}")


def update_values_db(values, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE {DB_TABLE} SET {values} WHERE id = {condition}")


def update_values_db_two(values, condition_name, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE {DB_TABLE} SET {values} WHERE {condition_name} = {condition}")
        # list_values_of_DB = f"user_channel='{user_channel}', channel_title='{channel_title}'"
        # update_values_db_two(list_values_of_DB, 'user_id', user_id_here)
        # Запрос текстовых полей
        # request_to_db_single_two('user_id', 'username', f"'{text_here}'")


def get_max_id(condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT MAX(id) FROM {DB_TABLE} WHERE user_id = {condition}")
        for z in cursor.fetchall():
            x = z[0]
        return x


def get_max_id_two(condition_name, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT MAX(id) FROM {DB_TABLE} WHERE {condition_name} = {condition}")
        for z in cursor.fetchall():
            x = z[0]
        return x


def request_to_db_single(request, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {request} FROM {DB_TABLE} WHERE id = {condition}")
        for z in cursor.fetchall():
            x = z[0]
            return x


def request_to_db_single_two(request, condition_name, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {request} FROM {DB_TABLE} WHERE {condition_name} = {condition}")
        for z in cursor.fetchall():
            x = z[0]
            return x


def request_to_db_multi(request, condition_name, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {request} FROM {DB_TABLE} WHERE {condition_name} = {condition}")
        return cursor.fetchall()
    # list_of_request = "id, is_payed, user_channel, reg_done, user_status"
    # sss = list(request_to_db_multi(list_of_request, 'user_id', user_id_here)[0])
    # id_here = sss[0]
    # is_payed = sss[1]


def request_to_db_column(request, condition_name, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {request} FROM {DB_TABLE} WHERE {condition_name} = {condition}")
        return cursor.fetchall()


def request_to_db_column_two(request, condition_name, condition, condition_name_2, condition_2):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {request} FROM {DB_TABLE} WHERE {condition_name} = '{condition}' AND {condition_name_2} = '{condition_2}'")
        # return cursor.fetchall()
        for z in cursor.fetchall():
            x = z[0]
            return x


# !!! Удаляет целую строку !!!
def delete_from_db(line_with_condition, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM {DB_TABLE} WHERE {line_with_condition} = '{condition}'")


def db_export():
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        # cursor.execute(f"SELECT * FROM {DB_TABLE}")
        cursor.execute(f"SELECT * FROM {DB_TABLE} ORDER BY date_of_use DESC")
        z = cursor.fetchall()
        return z


def db_export_short():
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id, user_id, username, first_name, last_name, age, sex, date_of_use, email, state_of_use, come_from FROM {DB_TABLE}")
        z = cursor.fetchall()
        return z
