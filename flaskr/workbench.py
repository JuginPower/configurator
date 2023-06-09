from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from stockmodels import Price, Indiz


work = Blueprint('workbench', __name__)
urlstring='http://stock.eugenkraft.com'


@work.route('/')
def index():
    return render_template('workbench/index.html')


@work.route('/monitor', methods=('GET', 'POST'))
@login_required
def monitor():
    if request.method == 'POST':
        id = request.form['id']
        amount = request.form['amount']
        price_object = Price(id)
        dates = price_object.get_dates(amount)
        prices = price_object.get_closes(amount)
        response_html = "<tr><th>Datum</th><th>Uhrzeit</th><th>Preis</th></tr>"
        for date, price in zip(dates, prices):
            # dateobj = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
            row = "<tr><td>" + date.strftime("%Y-%m-%d") + "</td><td>"+ date.strftime("%H:%M:%S") + "</td><td>" + str(price) + "</td></tr>"
            response_html += row
        return response_html
    
    indizData = get_indiz_data()
    return render_template('workbench/monitor.html', indizdata=indizData)


@work.route('/indicator')
def indicator():
    indizData = get_indiz_data()
    return render_template('workbench/indicator.html', indizdata=indizData)


def get_indiz_data(id=None, name=None):

    data = {}
    indiz_object = Indiz()
    
    if id:
        data.update({"name": indiz_object.get_one_name(id)})
    if name:
        data.update({"id": indiz_object.get_one_id(name)})
    if not id and not name:
        data.update({"ids": indiz_object.get_ids(), "names": indiz_object.get_names()})

    return data
