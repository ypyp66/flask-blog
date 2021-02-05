import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
import pymysql

bp = Blueprint('board', __name__, url_prefix='/boards')

@bp.route('/') #모든 게시판 목록
def index():
    db = get_db()
    boards = db.execute(
        ' SELECT title, body, created, author_id, board_id'
        ' FROM posts p'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('board/index.html', boards=boards)

@bp.route('/1') # 1번 게시판 목록
def board1():
    db = get_db()
    boards = db.execute(
        ' SELECT id, title, body, created, author_id'
        ' FROM posts p'
        ' WHERE board_id = 1'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('board/board1.html', boards=boards, board_id =1)

@bp.route('/2') # 2번 게시판 목록
def board2():
    db = get_db()
    boards = db.execute(
        ' SELECT id, title, body, created, author_id'
        ' FROM posts p'
        ' WHERE board_id = 2'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('board/board2.html', boards=boards, board_id =2)