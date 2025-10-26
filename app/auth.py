# INF601 - Advanced Programming in Python
# Iris Perry
# Mini Project 3

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('inventory.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inventory.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/profile')
def profile():
    if g.user is None:
        return redirect(url_for('auth.login'))
    return render_template('auth/profile.html')

@bp.route('/change-password', methods=('GET', 'POST'))
@login_required
def change_password():
    if request.method == 'POST':
        current = request.form.get('current_password')
        new = request.form.get('new_password')
        confirm = request.form.get('confirm_password')
        error = None

        if not current:
            error = 'Current password is required.'
        elif not new:
            error = 'New password is required.'
        elif new != confirm:
            error = 'New passwords do not match.'
        else:
            db = get_db()
            user = db.execute('SELECT * FROM user WHERE id = ?', (g.user['id'],)).fetchone()
            if user is None or not check_password_hash(user['password'], current):
                error = 'Current password is incorrect.'

        if error is None:
            db.execute(
                'UPDATE user SET password = ? WHERE id = ?',
                (generate_password_hash(new), g.user['id'])
            )
            db.commit()
            flash('Password changed successfully.')
            return redirect(url_for('auth.profile'))

        flash(error)

    # For GET or after flashing an error, show profile page (profile route will render template)
    return redirect(url_for('auth.profile'))
