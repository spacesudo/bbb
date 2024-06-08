import sqlite3


class Users:


    def __init__(self, dbname = "users.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)


    def setup(self):
        statement1 = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, chatid INTEGER UNIQUE, wallet TEXT DEFAULT '0x000' )"
        self.conn.execute(statement1)
        self.conn.commit()


    def add_user(self, username_):
        statement = "INSERT OR IGNORE INTO users (chatid) VALUES (?)"
        args = (username_, )
        self.conn.execute(statement, args)
        self.conn.commit()


    def update_wallet(self, wallet, userid):
        statement = "UPDATE users SET wallet = ? WHERE chatid = ?"
        args = (wallet, userid)
        self.conn.execute(statement, args)
        self.conn.commit()



    def get_wallet(self, owner):
        statement = "SELECT wallet FROM users WHERE chatid = ?"
        args = (owner,)
        cursor = self.conn.execute(statement, args)
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


    def get_users(self):
        statement = "SELECT chatid FROM users"
        return [x[0] for x in self.conn.execute(statement)]



class Bridge:
    
    def __init__(self, dbname="bridge.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        statement1 = """CREATE TABLE IF NOT EXISTS userdata (
                            id INTEGER PRIMARY KEY,
                            chatid INTEGER UNIQUE,
                            txid TEXT DEFAULT 'YES',
                            amount FLOAT DEFAULT 0.0
                        )"""
        self.conn.execute(statement1)
        self.conn.commit()

    def add_user(self, chatid):
        statement = "INSERT OR IGNORE INTO userdata (chatid) VALUES (?)"
        args = (chatid,)
        self.conn.execute(statement, args)
        self.conn.commit()

    def update_txid(self, txid, userid):
        statement = "UPDATE userdata SET txid = ? WHERE chatid = ?"
        args = (txid, userid)
        self.conn.execute(statement, args)
        self.conn.commit()

    def get_txid(self, userid):
        statement = "SELECT txid FROM userdata WHERE chatid = ?"
        args = (userid,)
        cursor = self.conn.execute(statement, args)
        result = cursor.fetchone()
        if result:
            return result[0]
        return None

    def update_amount(self, amount, userid):
        statement = "UPDATE userdata SET amount = ? WHERE chatid = ?"
        args = (amount, userid)
        self.conn.execute(statement, args)
        self.conn.commit()

    def get_amount(self, userid):
        statement = "SELECT amount FROM userdata WHERE chatid = ?"
        args = (userid,)
        cursor = self.conn.execute(statement, args)
        result = cursor.fetchone()
        if result:
            return result[0]
        return None

    def del_user(self, userid):
        statement = "DELETE FROM userdata WHERE chatid = ?"
        args = (userid,)
        self.conn.execute(statement, args)
        self.conn.commit()