from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import requests


work = Blueprint('workbench', __name__)
urlstring='http://127.0.0.2:5000'


@work.route('/')
def index():
    return render_template('workbench/index.html')


@work.route('/monitor', methods=('GET', 'POST'))
@login_required
def monitor():
    if request.method == 'POST':
        indiz_value = request.form['indiz']
        return render_template('workbench/results.html', indizvalue=indiz_value)
    
    indizdata = {"ids": get_id(), "names": get_name()}
    return render_template('workbench/monitor.html', indizdata=indizdata)


@work.route('/indicator')
@login_required
def indicator():
    return render_template('workbench/indicator.html')


def get_id(name=None):
    
    if name:
        return requests.get(urlstring + f"/id/{name}").json()
    else:
        return requests.get(urlstring + f"/id").json()


def get_name(id=None):

    if id:
        return requests.get(urlstring + f"/name/{id}").json()
    else:
        return requests.get(urlstring + f"/name").json()


def get_indiz(id=None):

    if id:
        return requests.get(urlstring + f"/indiz/{id}").json()
    else:
        return requests.get(urlstring + "/indiz").json()
