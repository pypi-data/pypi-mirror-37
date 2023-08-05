import sqlite3
import os
import pkg_resources


def get_db(db_path=None):
    """ returns a connection to the database """
    db_path = db_path or os.path.join(os.environ["HOME"], ".todolist.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """ initialize database """
    conn = get_db()
    query = pkg_resources.resource_string(__name__, "init_db.sql")
    conn.executescript(query.decode("utf-8"))


def add_todolist(name, description=None):
    """ add a todolist """
    conn = get_db()
    with conn:
        conn.execute("INSERT INTO todolist (name, description) values (?, ?)", (name, description))


def add_todo(name, todolist_id, description=None, deadline=None, status=0):
    """ add a todo to a todolist """
    conn = get_db()
    query = """
        INSERT INTO todo (name, description, deadline, status, todolist_id) 
        values (?, ?, ?, ?, ?)
    """

    with conn:
        conn.execute(query, (name, description, deadline, status, todolist_id))


def get_all_todolist():
    conn = get_db()
    with conn:
        results = conn.execute("SELECT * FROM todolist")
    return results


def get_todos(todolist_id):
    conn = get_db()
    with conn:
        results = conn.execute("SELECT * FROM todo where todolist_id = ?", (todolist_id,))

    return results

def get_todolist(todolist_id):
    conn = get_db()
    with conn:
        return conn.execute("SELECT * FROM todolist where id = ?", (todolist_id, )).fetchone()
