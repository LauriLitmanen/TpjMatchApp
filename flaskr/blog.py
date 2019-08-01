from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,jsonify
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, outCome,bestOf,enemy,score,league,mapOne,mapTwo,mapThree, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/api/data')
def data():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, outCome,bestOf,enemy,score,league,mapOne,mapTwo,mapThree, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    items = []
    for row in posts:
        items.append({'outCome':row[1], 'bestOf':row[2], 'enemy':row[3],'score':row[4],'league':row[5], 'mapOne':row[6], 'mapTwo':row[7], 'mapThree':row[8],'created':row[9]})
    return jsonify(items)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        outCome = request.form['outCome']
        bestOf = request.form['bestOf']
        enemy = request.form['enemy']
        score = request.form['score']
        league = request.form['league']
        mapOne = request.form['mapOne']
        mapTwo = request.form['mapTwo']
        mapThree = request.form['mapThree']
        error = None

        if not outCome:
            error = 'Outcome is required.'

        if not bestOf:
            error = 'Best of info required'

        if not enemy:
            error = 'Enemy is required'

        if not score:
            error = 'Score is required'

        if not league:
            error = 'League is required'

        if not mapOne:
            error = 'Atleast one map required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (outCome,bestOf,enemy,score,league,mapOne,mapTwo,mapThree, author_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (outCome, bestOf, enemy, score, league, mapOne, mapTwo, mapThree, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, outCome, bestOf, enemy, score, league, mapOne, mapTwo, mapThree, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        outCome = request.form['outCome']
        bestOf = request.form['bestOf']
        enemy = request.form['enemy']
        score = request.form['score']
        league = request.form['league']
        mapOne = request.form['mapOne']
        mapTwo = request.form['mapTwo']
        mapThree = request.form['mapThree']
        error = None

        if not outCome:
            error = 'Outcome is required.'

        if not bestOf:
            error = 'Best of info required'

        if not enemy:
            error = 'Enemy is required'

        if not score:
            error = 'Score is required'

        if not league:
            error = 'League is required'

        if not mapOne:
            error = 'Atleast one map required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET outCome = ?, bestOf = ?, enemy = ?, score = ?, league = ?, mapOne = ?, mapTwo = ?, mapThree = ?'
                ' WHERE id = ?',
                (outCome, bestOf, enemy, score, league, mapOne, mapTwo, mapThree, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
