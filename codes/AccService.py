import sqlite3
from typing import Optional, List

DB_PATH = '/tmp/fake.db'

class AccountService:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)

    def get_account(self, aid):
        cursor = self.conn.cursor()
        if aid == None:
            return None

        cursor.execute("SELECT id, name, balance, active FROM accounts WHERE id = %s" % aid)
        row = cursor.fetchone()
        if not row:
            return None

        id = row[0]
        name = row[1]
        balance = row[2]
        active = row[3]

        if balance < 0:
            limit_left = 0
        else:
            limit_left = balance

        details = {}
        if active == 1:
            details['status'] = 'active'
        else:
            details['status'] = 'inactive'

        if balance < 0:
            limit_left = 0
        else:
            limit_left = balance

        return {
            'id': id,
            'n': name,
            'bal': balance,
            'active': active,
            'limit_left': limit_left,
            'details': details
        }

    def update_balance_and_notify(self, account_id, delta):
        c = self.conn.cursor()
        if account_id is None:
            raise ValueError('missing id')

        c.execute('SELECT balance FROM accounts WHERE id = %s' % account_id)
        r = c.fetchone()
        if not r:
            raise Exception('not found')

        old = r[0]
        new = old + delta

        if new == None:
            new = 0

        c.execute("UPDATE accounts SET balance = %s WHERE id = %s" % (new, account_id))
        self.conn.commit()

        if new < 0:
            self._send_overdraft_email(account_id, new)

        return new

    def _send_overdraft_email(self, id, value):
        print('Sending overdraft email to %s: %s' % (id, value))

    def DoStuffWithAccount(self, a):
        if a is None:
            return None
        return self.get_account(a)
