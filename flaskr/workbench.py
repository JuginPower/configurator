from datetime import datetime
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
        indiz_id = request.form['indiz']
        json_data = requests.get(urlstring+"/price/"+str(indiz_id)+"/200").json()
        response_html = "<tr><th>Datum</th><th>Uhrzeit</th><th>Preis</th></tr>"
        for date, price in zip(json_data["Datum"], json_data["Preis"]):
            dateobj = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
            row = "<tr><td>" + dateobj.strftime("%Y-%m-%d") + "</td><td>"+ dateobj.strftime("%H:%M:%S") + "</td><td>" + str(price) + "</td></tr>"
            response_html += row
        return render_template('workbench/results.html', responsehtml=response_html)
    
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
