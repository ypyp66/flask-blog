import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
import pymysql

bp = Blueprint('auth', __name__, url_prefix='/auth')
@bp.route('/register', methods=('GET', 'POST')) #회원가입
def register():
    if request.method == 'POST':
        userId = request.form['userid']
        userPassword = request.form['userpwd']
        userEmail = request.form['useremail']
        db = get_db()
        error = None

        if not userId:
            error = 'Username is required.'
        elif not userPassword:
            error = 'Password is required.'
        elif not userEmail:
            error = 'Email is required'
        elif db.execute(
            'SELECT id FROM users WHERE userId = ?', (userId,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(userId)

        if error is None:
            db.execute(
                'INSERT INTO users (userId, userEmail, userPassword) VALUES (?, ?, ?)',
                (userId, userEmail,generate_password_hash(userPassword))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST')) #로그인
def login():
    if request.method == 'POST':
        userId = request.form['userId']
        userPassword = request.form['userPwd']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE userId = ?', (userId,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['userPassword'], userPassword):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('toHome'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user(): #무조건 먼저 실행
    #세션에 저장되어있는 사용자 user_id 를 가져오고, 이를 g.user에 저장
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('toHome'))

def login_required(view): #로그인이 필요한 항목이면
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view