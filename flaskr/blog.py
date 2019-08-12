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
        ' FROM result p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    posts_upcoming = db.execute(
        'SELECT p.id,upcoming_match_day, upcoming_startTime,upcoming_bestOf,upcoming_enemy,upcoming_league,upcoming_stage, created, author_id, username'
        ' FROM upcoming p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html',upcoming=posts_upcoming, results=posts)

@bp.route('/api/data/results')
def results_data():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, outCome,bestOf,enemy,score,league,mapOne,mapTwo,mapThree, created, author_id, username'
        ' FROM result p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    items = []
    for row in posts:
        items.append({'outCome':row[1], 'bestOf':row[2], 'enemy':row[3],'score':row[4],'league':row[5], 'mapOne':row[6], 'mapTwo':row[7], 'mapThree':row[8],'created':row[9]})
    return jsonify(items)

@bp.route('/api/data/upcoming')
def upcoming_data():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, upcoming_match_day,upcoming_startTime,upcoming_enemy,upcoming_league,upcoming_league,upcoming_bestOf,upcoming_stage, author_id, username'
        ' FROM upcoming p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    items = []
    for row in posts:
        items.append({'upcoming_match_day':row[1], 'upcoming_startTime':row[2], 'upcoming_enemy':row[3],'upcoming_league':row[4],'upcoming_bestOf':row[5], 'upcoming_stage':row[6],'created':row[9]})
    return jsonify(items)


@bp.route('/create_result', methods=('GET', 'POST'))
@login_required
def create_result():
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
                'INSERT INTO result (outCome,bestOf,enemy,score,league,mapOne,mapTwo,mapThree, author_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (outCome, bestOf, enemy, score, league, mapOne, mapTwo, mapThree, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create_result.html')


@bp.route('/create_upcoming', methods=('GET', 'POST'))
@login_required
def create_upcoming():
    if request.method == 'POST':

        match_day = request.form['match_day']
        startTime = request.form['startTime']
        enemy = request.form['enemy']
        league = request.form['league']
        bestOf = request.form['bestOf']
        stage = request.form['stage']

        error = None


        if not match_day:
            error = 'Match day is required'

        if not startTime:
            error = 'Starting time is required'

        if not enemy:
            enemy = 'TBA'

        if not bestOf:
            bestOf = 'TBA'

        if not stage:
            error = 'Stage is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO upcoming (upcoming_match_day, upcoming_startTime,upcoming_enemy,upcoming_league,upcoming_bestOf,upcoming_stage, author_id)'
                ' VALUES (?, ?, ?, ?, ?, ?,?)',
                (match_day,startTime,enemy,league,bestOf,stage, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create_upcoming.html')

def get_result(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, outCome, bestOf, enemy, score, league, mapOne, mapTwo, mapThree, created, author_id, username'
        ' FROM result p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

def get_upcoming(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, upcoming_match_day,upcoming_startTime,upcoming_enemy,upcoming_league,upcoming_league,upcoming_bestOf,upcoming_stage, author_id, username'
        ' FROM upcoming p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/result/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update_result(id):
    post = get_result(id)

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
                'UPDATE result SET outCome = ?, bestOf = ?, enemy = ?, score = ?, league = ?, mapOne = ?, mapTwo = ?, mapThree = ?'
                ' WHERE id = ?',
                (outCome, bestOf, enemy, score, league, mapOne, mapTwo, mapThree, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update_result.html', post=post)

@bp.route('/upcoming/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update_upcoming(id):
    post = get_upcoming(id)

    if request.method == 'POST':
        match_day = request.form['match_day']
        startTime = request.form['startTime']
        enemy = request.form['enemy']
        league = request.form['league']
        bestOf = request.form['bestOf']
        stage = request.form['stage']


        error = None

        if not match_day:
            error = 'Match day is required'

        if not startTime:
            error = 'Starting time is required'

        if not enemy:
            enemy = 'TBA'

        if not bestOf:
            bestOf = 'TBA'

        if not stage:
            error = 'Stage is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE upcoming SET upcoming_match_day = ?, upcoming_startTime = ?, upcoming_enemy = ?, upcoming_league = ?, upcoming_bestOf = ?, upcoming_stage = ?'
                ' WHERE id = ?',
                (match_day, startTime, enemy, league, bestOf, stage, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update_upcoming.html', post=post)

@bp.route('/result/<int:id>/delete', methods=('POST',))
@login_required
def delete_result(id):
    get_result(id)
    db = get_db()
    db.execute('DELETE FROM result WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route('/upcoming/<int:id>/delete', methods=('POST',))
@login_required
def delete_upcoming(id):
    get_upcoming(id)
    db = get_db()
    db.execute('DELETE FROM upcoming WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
