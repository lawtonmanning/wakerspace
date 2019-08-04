from datetime import datetime as dt

from wakerspace import app, db
from flask import render_template, redirect, request, url_for, session

from wakerspace.forms import IDForm, MakerForm
from wakerspace.models import Maker, Visit


@app.route('/')
def index():
    return redirect('/scan')


@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if 'RFID' in session: session.pop('RFID')
    if 'WFUID' in session: session.pop('WFUID')
    if 'maker' in session: session.pop('maker')

    form = IDForm(6)
    
    if form.validate_on_submit():
        session['RFID'] = form.integer.data
        maker = Maker.query.filter_by(rfid=form.integer.data).first()
        if maker:
            session['maker'] = maker.id
            return redirect('/maker')
        else:
            return redirect('/manual')
        
    return render_template('scan.html', form=form, label="Scan Badge")

@app.route('/manual', methods=['GET', 'POST'])
def manual():
    form = IDForm(8)
    
    if form.validate_on_submit():
        session['WFUID'] = form.integer.data
        maker = Maker.query.get(form.integer.data)
        if maker:
            if 'RFID' in session:
                maker.rfid = session['RFID']
                db.session.add(maker)
                db.session.commit()
            session['maker'] = maker.id
            return redirect('/maker')
        else:
            return redirect('/create')

    return render_template('manual.html', form=form, label="WFU ID")

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'WFUID' not in session:
        return redirect('/scan')

    form = MakerForm()
    maker = Maker()
    maker.id = session['WFUID']
    if 'RFID' in session: maker.rfid = session['RFID']
    
    if form.validate_on_submit():
        maker.first_name = form.first_name.data
        maker.last_name = form.last_name.data

        db.session.add(maker)
        db.session.commit()

        session['maker'] = maker.id
        return redirect('/maker')
    
    return render_template('create.html', form=form)

@app.route('/maker', methods=['GET', 'POST'])
def maker():
    if 'maker' not in session:
        return redirect('/scan')
    
    maker = Maker.query.get(session['maker'])
    if not maker:
        return redirect('/scan')

    role = 'Maker'

    form = MakerForm()

    return render_template('maker.html', form=form, maker=maker, role=role)
