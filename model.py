import sqlite3

class ResourcesDAO:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ResourcesDAO, cls).__new__(cls)
            print('DAO - New instance created')
        return cls._instance

    def __init__(self, db_file):
        if not hasattr(self, 'conn'):
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
            print('DB - Connection established')
            self.create_table()

    def create_table(self):
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS RESOURCES (
                    RESOURCE_CODE TEXT PRIMARY KEY NOT NULL,
                    RESOURCE_GROUP TEXT,
                    SHORT_CODE TEXT,
                    RESOURCE_NAME TEXT,
                    UNIT TEXT,
                    STD_RATE REAL,
                    PROJECT_RATE REAL,
                    CONSUMPTION REAL,
                    PRODUCTION REAL
                )
            ''')
        self.conn.commit()
        print('DB - create table function executed')

    def insert_resource(self, resource_data):
        sql = '''
            INSERT INTO RESOURCES (
                RESOURCE_CODE,
                RESOURCE_GROUP,
                SHORT_CODE,
                RESOURCE_NAME,
                UNIT,
                STD_RATE,
                PROJECT_RATE,
                CONSUMPTION,
                PRODUCTION
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(sql, resource_data)
        self.conn.commit()
        print('DB - Record inserted')

    def get_resource_by_code(self, resource_code):
        sql = 'SELECT * FROM RESOURCES WHERE RESOURCE_CODE = ?'
        self.cursor.execute(sql, (resource_code,))
        print('DB - fetched record')
        return self.cursor.fetchone()

    print('DB - RESOURCES table created')

    def update_resource(self, resource_code, resource_data):
        sql = '''
            UPDATE RESOURCES SET
                RESOURCE_NAME = ?,
                UNIT = ?,
                STD_RATE = ?,
                PROJECT_RATE = ?,
                CONSUMPTION = ?,
                PRODUCTION = ?
            WHERE RESOURCE_CODE = ?
        '''
        self.cursor.execute(sql, (*resource_data, resource_code))
        self.conn.commit()
        print('DB - Updated a record')

    def delete_resource(self, resource_code):
        sql = 'DELETE FROM RESOURCES WHERE RESOURCE_CODE = ?'
        self.cursor.execute(sql, (resource_code,))
        self.conn.commit()
        print('DB - Deleted a record')

    def get_all_resources(self):
        sql = 'SELECT * FROM RESOURCES  ORDER BY 1'
        self.cursor.execute(sql)
        print('DB - Fetched all records')
        return self.cursor.fetchall()

    def get_table_headers(self, table_name="RESOURCES"):
        self.cursor.execute("PRAGMA table_info(%s)" % table_name)
        headers = [row[1] for row in self.cursor.fetchall()]
        print('DB - Fetched table headers')
        return headers

    def __del__(self):
        self.conn.close()
        self.conn.close()
        print('DB - Connection closed')
