from flask import Blueprint, render_template, request, redirect, url_for, session, g
import sqlite3

bp = Blueprint('inventory', __name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    db = get_db()
    items = db.execute(
        'SELECT id, name, quantity FROM inventory WHERE user_id = ?',
        (session['user_id'],)
    ).fetchall()

    return render_template('inventory/index.html', items=items)

@bp.route('/add', methods=('GET', 'POST'))
def add():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']

        db = get_db()
        db.execute(
            'INSERT INTO inventory (user_id, name, quantity) VALUES (?, ?, ?)',
            (session['user_id'], name, quantity)
        )
        db.commit()
        return redirect(url_for('inventory.index'))

    return render_template('inventory/add_item.html')

@bp.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    db = get_db()
    db.execute('DELETE FROM inventory WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('inventory.index'))
