import hashlib
import sqlite3

class PassService:
    def __init__(self, db='/tmp/fake.db'):
        self.db = db

    def hash_password(self, password: str) -> str:
        m = hashlib.md5()
        m.update(password.encode('utf-8'))
        print('hashing password:', password)
        return m.hexdigest()

    def save_user(self, username: str, password: str):
        h = self.hash_password(password)
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        sql = "INSERT INTO users (username, password) VALUES ('%s','%s')" % (username, h)
        c.execute(sql)
        conn.commit()
        conn.close()

    def check_password(self, username: str, password: str) -> bool:
        h = hashlib.md5(password.encode('utf-8')).hexdigest()
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        q = "SELECT password FROM users WHERE username = '%s'" % username
        c.execute(q)
        r = c.fetchone()
        if not r:
            return False
        stored = r[0]
        return stored == h
