import MySQLdb

class Database(object):
    def __init__(self, host, user, db_name, table, db=None):
        self.host = host
        self.user = user
        self.db_name = db_name
        self.table = table
        self.db = Database.connect(self)


    def connect(self): 
        db = MySQLdb.connect(host=self.host,
                     user=self.user,
                     passwd="password",
                     db=self.db_name)
        return db


    def create(self, username):
        cursor = self.db.cursor()
        cursor.execute("show tables");
        tables = cursor.fetchall();
        exists = False
        for table in tables:
            if table[0] == username:
                exists = True
                return exists
        if exists == False:
            cursor.execute(f"create table {username}(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, problem_name VARCHAR(30), language VARCHAR(30), submission_id VARCHAR(30), problem_status VARCHAR(10));")
            return exists

    def show(self):
        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM {self.table};")
        return cursor.fetchall()

    def insert(self, problem, language, files, id, status):
        cursor = self.db.cursor()
        cursor.execute(f"INSERT INTO {self.table}(problem_name, language, submission_id, problem_status) VALUES ('{problem}', '{language}',  '{id}', '{status}');")
        self.db.commit()

    def show_accepted(self):
        cursor = self.db.cursor()
        cursor.execute(f"SELECT problem_name FROM {self.table} WHERE problem_status='Accepted' GROUP BY problem_name;")
        return cursor.fetchall()

    def count_accepted(self):
        data = Database.show_accepted()
        return sum([1 for i in data[0]])

