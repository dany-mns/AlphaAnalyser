import mysql.connector
from src.message import Message

class Database:
    def __init__(self, username, password, database_name):
        self.mydb = mysql.connector.connect(host="localhost", user=username, password=password, database=database_name)
        self.cursor = self.mydb.cursor()
        self.users = []

    def get_messages(self):
        history = {}
        self.cursor.execute("SELECT * FROM Messages")
        result = self.cursor.fetchall()
        for r in result:
            if r[1] not in history.keys():
                history[r[1]] = []
            history[r[1]].append(Message(r[2], r[3], r[4]))
        return history

    def get_users(self):
        self.cursor.execute("SELECT username from Users")
        result = self.cursor.fetchall()
        self.users = [r[0] for r in result]
        return self.users

    # write result
    def write_data(self):
        pass