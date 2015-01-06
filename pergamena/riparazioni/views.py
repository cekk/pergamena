# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)

blueprint = Blueprint("riparazioni", __name__, url_prefix='/riparazioni',
                        static_folder="../static")


from pergamena.riparazioni.models import Riparazione, Categoria
from pergamena.riparazioni.forms import InsertRiparazioneForm
from pergamena.riparazioni.forms import CompletaRiparazioneForm
from pergamena.riparazioni.forms import ImportDb
from pergamena.riparazioni.forms import Search
from pergamena.utils import flash_errors
from pergamena.database import db
from flask.ext.login import login_required
from flask.views import MethodView
from werkzeug import secure_filename
from csv import reader, DictReader
import datetime
from sqlalchemy_searchable import search


@blueprint.route("/nuova_riparazione", methods=['GET', 'POST'])
@login_required
def nuova_riparazione():
    if request.form.get('btn-annulla', ''):
        flash("Creazione annullata", 'success')
        return redirect(url_for('public.home'))
    form = InsertRiparazioneForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_riparazione = Riparazione.create(**form.data)
        flash("Riparazione inserita con successo!", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('riparazioni/form_riparazione.html', form=form)


@blueprint.route("/modifica_riparazione/<id>", methods=['GET', 'POST'])
@login_required
def modifica_riparazione(id=None):
    if not id:
        flash(u'Devi fornire un id!', 'error')
    else:
        if request.form.get('btn-annulla', ''):
            flash("Modifica annullata", 'success')
            return redirect(url_for('public.home'))
        riparazione = Riparazione.query.get_or_404(id)
        values_dict = dict([(m.key, getattr(riparazione, m.key)) for m in riparazione.__table__.columns])
        form = CompletaRiparazioneForm(**values_dict)
        if form.validate_on_submit():
            data = form.data
            Riparazione.update(riparazione, **data)
            flash("Riparazione modificata con successo!", 'success')
            return redirect(request.referrer)
        else:
            flash_errors(form)
    return render_template('riparazioni/form_riparazione.html', form=form)


@blueprint.route("/completa_riparazione/<id>", methods=['GET', 'POST'])
@login_required
def completa_riparazione(id=None):
    if not id:
        flash(u'Devi fornire un id!', 'error')
    else:
        if request.form.get('btn-annulla', ''):
            flash("Modifica annullata", 'success')
            return redirect(url_for('public.home'))
        riparazione = Riparazione.query.get_or_404(id)
        values_dict = dict([(m.key, getattr(riparazione, m.key)) for m in riparazione.__table__.columns])
        form = CompletaRiparazioneForm(**values_dict)
        if form.validate_on_submit():
            data = form.data
            data['finito'] = True
            Riparazione.update(riparazione, **data)
            flash("Riparazione completata con successo!", 'success')
            return redirect(request.referrer)
        else:
            flash_errors(form)
    return render_template('riparazioni/form_riparazione.html', form=form)


@blueprint.route("/ricerca", methods=['GET', 'POST'])
@login_required
def ricerca():
    form = Search()
    riparazioni = []
    if form.validate_on_submit():
        data = form.data
        search_text = data.get('search_text')
        riparazioni = Riparazione.query.filter((Riparazione.cognome.ilike(search_text)) | (Riparazione.oggetto.ilike(search_text))).all()
    return render_template('riparazioni/search_form.html',
                           form=form,
                           riparazioni=riparazioni,
                           message="")

@blueprint.route("/riparazioni_pendenti", methods=['GET'])
@blueprint.route('/riparazioni_pendenti/<int:page>', methods=['GET'])
@login_required
def riparazioni_pendenti(page=1):
    riparazioni = Riparazione.query.filter_by(finito=False).order_by(Riparazione.data_arrivo.desc()).paginate(page, 20, False)
    return render_template("riparazioni/riparazioni_list.html",
                            riparazioni=riparazioni,
                            title="Riparazioni pendenti")

@blueprint.route("/riparazioni_completate", methods=['GET'])
@blueprint.route('/riparazioni_completate/<int:page>', methods=['GET'])
@login_required
def riparazioni_completate(page=1):
    riparazioni = Riparazione.query.filter_by(finito=True).order_by(Riparazione.data_riparazione.desc()).paginate(page, 20, False)
    return render_template("riparazioni/riparazioni_list.html",
                           riparazioni=riparazioni,
                           title="Riparazioni completate")

@blueprint.route('/delete/<id>')
@login_required
def delete_item(id=None):
    if not id:
        flash(u'Devi fornire un id!', 'error')
    else:
        riparazione = Riparazione.query.get_or_404(id)
        riparazione.delete()
        flash(u'Riparazione eliminata.', 'success')
    return redirect(request.referrer)

REFACTORED_FIELDS = (('riparaz_eff', 'riparazione_effettuata'),
                     ('spese_sped', 'spese_spedizione'),
                     ('cat', 'categoria'),
                     ('descr', 'descrizione'),
                     ('tot', 'totale'),
                     ('costo_rip', 'costo_riparazione'),
                     ('ref', 'referenza'),
                     ('consegna', 'consegna_prevista'),
                     ('data_riparaz', 'data_riparazione'),
                     ('n_rip', 'n_riparazione'))

DATE_FIELDS = ('data_riparazione', 'consegna_prevista', 'data_arrivo')
FLOAT_FIELDS = ('peso', 'preventivo', 'costo_riparazione', 'spese_spedizione',
                'totale')
STRING_FIELDS = ('cognome', 'nome', 'indirizzo', 'citta', 'telefono',
                 'cell', 'categoria', 'oggetto', 'descrizione', 'referenza',
                 'difetto', 'riparatore', 'n_riparazione',
                 'riparazione_effettuata', 'garanzia', 'note')


@blueprint.route("/import_db/", methods=['GET', 'POST'])
@login_required
def import_db():
    form = ImportDb()
    if form.validate_on_submit():
        for riparazione in Riparazione.query.all():
            riparazione.delete()
        print "Riparazioni eliminate"
        filename = secure_filename(form.file.data.filename)
        csv = form.file.data.stream
        items = DictReader(csv)
        for item in items:
            if item.get('finito') == '1':
                item['finito'] = True
            else:
                item['finito'] = False
            del item['id_riparaz']
            for field_map in REFACTORED_FIELDS:
                item[field_map[1]] = item[field_map[0]]
                del item[field_map[0]]
            for field in DATE_FIELDS:
                if item.get(field) == '':
                    item[field] = None
                else:
                    try:
                        if len(item[field].split('/')[-1]) == 2:
                            splitted_date = item[field].split('/')
                            splitted_date[-1] = "20%s" % splitted_date[-1]
                            item[field] = ('/').join(splitted_date)
                        item[field] = datetime.date(*reversed(map(int, item[field].split('/'))))
                    except:
                        item[field] = None
            for field in STRING_FIELDS:
                item[field] = item[field].decode('windows-1252')
            new_riparazione = Riparazione.create(**item)
    else:
        flash_errors(form)
    return render_template('riparazioni/upload.html', form=form)
