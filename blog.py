from flask import ( Blueprint, flash, g, redirect, render_template, request, url_for ) 
from werkzeug.exceptions import abort 
from auth import login_required 
from db import get_db 


bp = Blueprint('blog', __name__)
@bp.route('/boards/<board_id>/<int:id>')
def index(board_id, id):
    # db의 정보를 가져옵니다.
    db = get_db()

    # 게시글 정보를 모두 가져오는 query를 실행
    post = db.execute(
        ' SELECT id, title, body, created, author_id'
        ' FROM posts'
        ' WHERE posts.id = ?', (id,)
    ).fetchall()

    # board/index.html로 정보를 보냅니다.
    return render_template('blog/index.html', board_id=board_id,posts=post)

@bp.route('/boards/<board_id>/create', methods=('GET', 'POST'))
@login_required
def create(board_id):
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO posts (title, body, author_id, board_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['userId'], board_id)
            )
            db.commit()
            return redirect(url_for(f'board.board{board_id}'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT title, body, author_id, created'
        ' FROM posts p JOIN users u ON p.author_id = u.userId'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['userId']:
        abort(403)

    return post

@bp.route('/boards/<board_id>/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(board_id, id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE posts SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index', board_id=board_id, id=id))

    return render_template('blog/update.html', post=post)

@bp.route('/boards/<board_id>/<int:id>/delete')
@login_required
def delete(board_id, id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for(f'board.board{board_id}'))