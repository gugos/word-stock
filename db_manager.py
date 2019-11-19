import sqlite3
import string

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

    def get_records(self, table_name):
        query = f'SELECT * FROM {table_name} ORDER BY word desc'
        result = self.execute_db_query(query)
        records = []
        for record in result:
            records.append(record)
        return records

    def save_record(self, table_name, parameters):
        query = f'INSERT INTO {table_name} VALUES(?, ?, ?, ?)'
        self.execute_db_query(query, parameters)

    def update_record(self, table_name, word, parameters):
        query = f'UPDATE {table_name} SET definition=?, additional_info=?, score=? WHERE word=\'{word}\''
        self.execute_db_query(query, parameters)

    def delete_record(self, table_name, word):
        query = f'DELETE FROM {table_name} WHERE word=\'{word}\''
        self.execute_db_query(query)

    def record_exists(self, table_name, word):
        query = f'SELECT COUNT(1) FROM {table_name} WHERE word=\'{word}\''
        result = self.execute_db_query(query)
        for record in result:
            return True if 1 in record else False

    def get_records_count(self):
        count = 0
        for table_name in list(string.ascii_uppercase):
            query = f'SELECT COUNT(*) FROM {table_name}'
            result = self.execute_db_query(query)
            for record in result:
                count += record[0]
        return count

    def get_records_count_by_score_range(self, parameters):
        count = 0
        for table_name in list(string.ascii_uppercase):
            query = f'SELECT COUNT(*) FROM {table_name} WHERE score BETWEEN ? AND ?'
            result = self.execute_db_query(query, parameters)
            for record in result:
                count += record[0]
        return count

    def get_all_records_by_score_range(self, parameters):
        records = []
        for table_name in list(string.ascii_uppercase):
            query = f'SELECT word, definition, score FROM {table_name} WHERE score BETWEEN ? AND ?'
            result = self.execute_db_query(query, parameters)
            for record in result:
                records.append(record)
        return records

    def get_random_records_by_score_range(self, parameters):
        records = []
        for table_name in list(string.ascii_uppercase):
            query = f'SELECT word, definition, score FROM {table_name} WHERE score BETWEEN ? AND ? ORDER BY RANDOM() LIMIT ?'
            result = self.execute_db_query(query, parameters)
            for record in result:
                records.append(record)
        return records

    def update_score(self, table_name, word, score):
        query = f'UPDATE {table_name} SET score={score} WHERE word=\'{word}\''
        self.execute_db_query(query)

    # def create_tables(self):
    #     for table_name in list(string.ascii_uppercase):
    #         query = f'create table {table_name}' \
    #                 f'(' \
    #                 f'word string not null,' \
    #                 f'definition text not null,' \
    #                 f'additional_info text,' \
    #                 f'score real not null' \
    #                 f');'
    #         self.execute_db_query(query)
