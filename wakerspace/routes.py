from datetime import datetime as dt
from datetime import date as d

from wakerspace import app, db
from flask import render_template, redirect, request, url_for, session

from wakerspace.forms import IDForm, MakerForm, EditMakerForm, TrainingsForm, CheckInForm
from wakerspace.models import Maker, Visit, Training, Room, Equipment


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

    return render_template('manual.html', form=form, label="WFU ID", cancel='/')

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
        maker.classification = form.classification.data
        if form.classification.data == 'STUDENT':
            maker.year = form.year.data

        maker.staff = form.staff.data
        if maker.staff:
            staff_training = Training()
            staff_training.maker_id = maker.id
            staff_training.equipment_id = Equipment.query.filter_by(type='Staff').first().id
            staff_training.date = d.today()
            db.session.add(staff_training)

        db.session.add(maker)
        db.session.commit()

        session['maker'] = maker.id
        return redirect('/maker')
    
    return render_template('create.html', form=form, cancel='/')

@app.route('/maker', methods=['GET', 'POST'])
def maker():
    if 'maker' not in session:
        return redirect('/scan')
    
    maker = Maker.query.get(session['maker'])
    if not maker:
        return redirect('/scan')
    
    form = EditMakerForm()
    
    num_cols = len(Room.query.all())

    if form.validate_on_submit():
        value = request.form['submit']
        direct = '/'
        if value.startswith('Check'):
            if value == 'Check-In':
                direct = '/in'
            elif value == 'Check-Out':
                visit = maker.last_visit()
                visit.out_time = dt.utcnow()
                db.session.add(visit)
                db.session.commit()
        
        elif value == 'Add Training':
            direct = '/trainings' 
        
        return redirect(direct)

    return render_template('maker.html', form=form, maker=maker, num_cols=num_cols)

@app.route('/in', methods=['GET', 'POST'])
def insomething():
    if 'maker' not in session:
        return redirect('/scan')

    maker = Maker.query.get(session['maker'])
    if not maker:
        return redirect('/scan')

    
    form = CheckInForm()
    choices = []
    for training in maker.trainings:
        equipment = training.equipment
        if equipment.usable:
            choices.append((equipment.id, equipment.type))
    
    choices.append((0, 'Other'))
    form.purpose.choices = choices

    if form.validate_on_submit():
        visit = Visit()
        visit.maker_id = maker.id
        visit.in_time = dt.utcnow()
        visit.purpose = form.purpose.data
        if not visit.purpose:
            visit.purpose = None

        db.session.add(visit)
        db.session.commit()

        return redirect('/maker')

    return render_template('in.html', form=form, maker=maker, cancel='/maker')


@app.route('/trainings', methods=['GET', 'POST'])
def trainings():
    if 'maker' not in session:
        return redirect('/scan')

    maker = Maker.query.get(session['maker'])
    if not maker:
        return redirect('/scan')

    form = TrainingsForm()
    trainings = Equipment.query.all()
    for training in maker.trainings:
        trainings.remove(training.equipment)

    if not trainings:
        return redirect('/maker')

    form.trainings.choices = [(t.id, t.type) for t in trainings]

    if form.validate_on_submit():
        training = Training()
        training.maker_id = maker.id
        training.equipment_id = form.trainings.data
        training.date = d.today()

        db.session.add(training)
        db.session.commit()
        return redirect('/maker')

    return render_template('trainings.html', form=form, maker=maker, cancel='/maker')

