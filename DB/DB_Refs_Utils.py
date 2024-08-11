import psycopg

from Config.config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE, DB_TABLE_REFS


def add_all_to_db_refs(columns_here, data_here):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO {DB_TABLE_REFS} ({columns_here}) VALUES ({data_here})")


def request_to_db_single_refs(request, condition_name, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {request} FROM {DB_TABLE_REFS} WHERE {condition_name} = {condition}")
        for z in cursor.fetchall():
            x = z[0]
            return x


# Команда DISTINCT используется для удаления из выдачи дубликатов
def request_to_db_distinct_refs(request, condition_name, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        # cursor.execute(f"SELECT {request} FROM {DB_TABLE_REFS} WHERE {condition_name} = {condition}")
        cursor.execute(f"SELECT DISTINCT {request} FROM {DB_TABLE_REFS} WHERE {condition_name} = {condition} AND {request} IS NOT NULL")
        z = cursor.fetchall()
        return z


# Команда SUM() используется для суммирования выборки
def request_to_db_sum_refs(request, condition_name, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        # cursor.execute(f"SELECT {request} FROM {DB_TABLE_REFS} WHERE {condition_name} = {condition}")
        # cursor.execute(f"SELECT SUM({request}) FROM {DB_TABLE_REFS} WHERE {condition_name} = {condition}")
        cursor.execute(f"SELECT COALESCE(SUM({request})) FROM {DB_TABLE_REFS} WHERE {condition_name} = {condition}")
        for z in cursor.fetchall():
            x = z[0]
            return x


def request_to_db_sum_multi_refs(request, condition_name, condition, condition_name_2, condition_2):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        # cursor.execute(f"SELECT {request} FROM {DB_TABLE_REFS} WHERE {condition_name} = {condition}")
        # cursor.execute(f"SELECT SUM({request}) FROM {DB_TABLE_REFS} WHERE {condition_name} = {condition}")
        cursor.execute(f"SELECT COALESCE(SUM({request})) FROM {DB_TABLE_REFS} WHERE {condition_name} = {condition} AND {condition_name_2} = {condition_2}")
        for z in cursor.fetchall():
            x = z[0]
            return x


def get_max_id_refs(condition_name, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT MAX(id) FROM {DB_TABLE_REFS} WHERE {condition_name} = {condition}")
        for z in cursor.fetchall():
            x = z[0]
        return x


def update_values_db_refs(values, condition_name, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE {DB_TABLE_REFS} SET {values} WHERE {condition_name} = {condition}")
    # list_values_of_DB = f"bot_last_post='{post_id}'," \
    #                     f"channel_last_post='{message_id}'," \
    #                     f"date_of_use = '{date_time_2}'"
    # id_in_base = get_max_id(user_id)
    # update_values_db(list_values_of_DB, id_in_base)


def db_export_refs():
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {DB_TABLE_REFS}")
        # cursor.execute(f"SELECT * FROM {DB_TABLE_REFS} ORDER BY date_of_use DESC")
        z = cursor.fetchall()
        return z


def db_export_ref_vip(list_here, condition_name, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        # cursor.execute(f"SELECT id, referal, lead_1, paid_by_lead_1, date_of_pay_lead_1, sum_of_pay_lead_1, sum_to_ref_0, payout_lead_1_to_0, date_payout_lead_1_to_0, lead_2, paid_by_lead_2, date_of_pay_lead_2, sum_of_pay_lead_2, sum_to_ref_lead_2_to_0, sum_to_ref_lead_2_to_1, payout_lead_2_to_0, lead_1_username, lead_2_username, referal_username FROM {DB_TABLE_REFS}")
        cursor.execute(f"SELECT {list_here} FROM {DB_TABLE_REFS} WHERE {condition_name} = {condition}")

        z = cursor.fetchall()
        return z


def db_export_ref(list_here, condition_name, condition):
    connection = psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        # cursor.execute(f"SELECT id, referal, lead_1, paid_by_lead_1, date_of_pay_lead_1, sum_of_pay_lead_1, sum_to_ref_0, payout_lead_1_to_0, date_payout_lead_1_to_0, lead_2, paid_by_lead_2, date_of_pay_lead_2, sum_of_pay_lead_2, sum_to_ref_lead_2_to_0, sum_to_ref_lead_2_to_1, payout_lead_2_to_0, lead_1_username, lead_2_username, referal_username FROM {DB_TABLE_REFS}")
        cursor.execute(f"SELECT {list_here} FROM {DB_TABLE_REFS} WHERE {condition_name} = {condition} AND lead_2 IS NOT NULL")

        z = cursor.fetchall()
        return z
