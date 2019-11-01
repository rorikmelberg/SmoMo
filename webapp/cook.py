import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
# from . db import get_db

bp = Blueprint('cook', __name__, url_prefix='/cook')

@bp.route('/', methods=('GET', 'POST'))
def cook():
    if request.method == 'POST':
        username = request.form['title']
        db = get_db()
        error = None

        if not title:
            error = 'Please supply a title.'

        if error is None:
            db.execute('INSERT INTO Cook Values(Title)', (title))
            db.commit()
            return redirect(url_for('index'))

        flash(error)

    return render_template('startcook.html')