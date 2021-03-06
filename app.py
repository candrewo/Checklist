import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os

app = Flask(__name__)


app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'checklist.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('CHECKLIST_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, amount, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('home.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    db = get_db()
    db.execute('insert into entries (title, amount, text) values (?, ?, ?)',
                 [request.form['title'], request.form['amount'], request.form['text']])
    db.commit()
    flash('Added something else you cannot forget!')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    init_db()
    app.run()
