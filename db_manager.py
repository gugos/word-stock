import sqlite3

DB_NAME = 'db_dictionary'


class DBManager:
    def __init__(self):
        self.db_filename = DB_NAME

    def execute_db_query(self, query, parameters=()):
        with sqlite3.connect(self.db_filename) as connection:
            cursor = connection.cursor()
            query_result = cursor.execute(query, parameters)
            connection.commit()
        return query_result

    def get_records(self, letter):
        table_name = letter
        query = f'SELECT * FROM {table_name} ORDER BY word desc'
        return self.execute_db_query(query)

    def save_record(self, table_name, parameters):
        query = f'INSERT INTO {table_name} VALUES(?, ?, ?, ?)'
        self.execute_db_query(query, parameters)

    # def create_tables(self):
    #     import string
    #     for table_name in list(string.ascii_uppercase):
    #         query = f'create table {table_name}' \
    #                 f'(' \
    #                 f'word string not null,' \
    #                 f'definition text not null,' \
    #                 f'additional_info text,' \
    #                 f'score real not null' \
    #                 f');'
    #         self.execute_db_query(query)
