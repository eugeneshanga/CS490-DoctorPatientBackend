import pytest
import mysql.connector

# A fake cursor returning preconfigured rows and supporting insert/update metadata
class FakeCursor:
    def __init__(self, rows=None, dictionary=False):
        self._rows = rows or []
        self._dict = dictionary
        self.lastrowid = 0
        self.rowcount = 0

    def execute(self, query, params=None):
        q = query.strip().lower()
        # Simulate auth lookup: only recognized email logs in
        if q.startswith("select") and "from users" in q:
            email = params[0] if params else None
            if email == 'dr.house@example.com':
                self._rows = [{'user_id': 1, 'email': email, 'password': 'password'}]
            else:
                self._rows = []
            return
        # Simulate insert/update/delete affecting one row
        if q.startswith("insert"):
            self.lastrowid += 1
            self.rowcount = 1
        elif q.startswith("update") or q.startswith("delete"):
            self.rowcount = 1
        # For other SELECTs, use pre-set rows (tests override FakeConn._rows)
        return

    def fetchall(self):
        return self._rows

    def fetchone(self):
        return self._rows[0] if self._rows else None

    def close(self):
        pass

    # Context manager support for 'with conn.cursor() as cursor'
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

# A fake connection handing out the fake cursor and supporting context manager
class FakeConn:
    def __init__(self):
        self._rows = []
        self._cursor = FakeCursor(self._rows)

    def cursor(self, dictionary=False):
        self._cursor._dict = dictionary
        self._cursor.rowcount = 0
        return self._cursor

    def commit(self):
        pass

    def close(self):
        pass

    # context manager support for 'with mysql.connector.connect()'
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

@pytest.fixture(autouse=True)
def patch_mysql_connect(monkeypatch):
    """
    Automatically replace mysql.connector.connect with a fake connection.
    Tests can modify the returned FakeConn._rows to control SELECT results for non-auth code.
    Auth SELECTs are auto-handled.
    """
    fake_conn = FakeConn()
    monkeypatch.setattr(
        mysql.connector,
        'connect',
        lambda **kwargs: fake_conn
    )
    return fake_conn
