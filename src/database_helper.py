#%%
import sqlite3

class Database:
    def __init__(self, name):
        self._conn = sqlite3.connect(name)
        self._cursor = self._conn.cursor()
        #logging.info('Connected to database')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor
    
    def create_table(self, table_name, columns):
        self.execute_query(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        print(f"Table {table_name} created successfully")


    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()


    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query,params or ())
            self.connection.commit()
            print("Query executed successfully")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
    
    def execute_many(self, sql, params=None):
        self.cursor.executemany(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()
    
    def from_pandas(self, df, table_name, if_exists='replace'):
        self.execute('drop table if exists {}'.format(table_name))
        df.to_sql(table_name, self.connection, if_exists=if_exists, index=False)

# %%