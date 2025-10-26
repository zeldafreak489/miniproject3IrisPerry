# INF601 - Advanced Programming in Python
# Iris Perry
# Mini Project 3

from flask import Blueprint, render_template, request, redirect, url_for, session, g, abort
import sqlite3

bp = Blueprint('inventory', __name__, url_prefix='/inventory')

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

@bp.route('/<int:item_id>')
def details(item_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    db = get_db()
    item = db.execute(
        'SELECT * FROM inventory WHERE id = ? AND user_id = ?',
        (item_id, session['user_id'])
    ).fetchone()

    if item is None:
        abort(404)

    return render_template('inventory/details.html', item=item)

@bp.route('/<int:item_id>/edit', methods=('GET', 'POST'))
def edit(item_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    db = get_db()
    item = db.execute(
        'SELECT * FROM inventory WHERE id = ? AND user_id = ?',
        (item_id, session['user_id'])
    ).fetchone()

    if item is None:
        abort(404)

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']

        db.execute(
            'UPDATE inventory SET name = ?, quantity = ? WHERE id = ? AND user_id = ?',
            (name, quantity, item_id, session['user_id'])
        )
        db.commit()
        return redirect(url_for('inventory.index'))

    return render_template('inventory/edit_item.html', item=item)

@bp.route('/<int:item_id>/delete', methods=('POST',))
def delete(item_id):
    db = get_db()
    db.execute('DELETE FROM inventory WHERE id = ? AND user_id = ?', (item_id, session['user_id']))
    db.commit()
    return redirect(url_for('inventory.index'))
