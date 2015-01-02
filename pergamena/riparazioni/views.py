# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)

blueprint = Blueprint("riparazioni", __name__, url_prefix='/riparazioni',
                        static_folder="../static")


from pergamena.riparazioni.models import Riparazione
from pergamena.riparazioni.forms import InsertRiparazioneForm
from pergamena.riparazioni.forms import CompletaRiparazioneForm
from pergamena.utils import flash_errors
from pergamena.database import db
from flask.ext.login import login_required
from flask.views import MethodView


@blueprint.route("/nuova_riparazione", methods=['GET', 'POST'])
@login_required
def nuova_riparazione():
    form = InsertRiparazioneForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_riparazione = Riparazione.create(**form.data)
        flash("Riparazione inserita con successo!", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('riparazioni/form_riparazione.html', form=form)

@blueprint.route("/completa_riparazione/<id>", methods=['GET', 'POST'])
@login_required
def completa_riparazione(id=None):
    if not id:
        flash(u'Devi fornire un id!', 'error')
    else:
        riparazione = Riparazione.query.get_or_404(id)
        import pdb;pdb.set_trace()
        values_dict = dict([(m.key, getattr(riparazione, m.key)) for m in riparazione.__table__.columns])
        form = CompletaRiparazioneForm(obj=**values_dict, csrf_enabled=False)
        if form.validate_on_submit():
            Riparazione.update(**form.data)
            flash("Riparazione inserita con successo!", 'success')
            return redirect(url_for('public.home'))
        else:
            flash_errors(form)
    return render_template('riparazioni/form_riparazione.html', form=form)

@blueprint.route("/ricerca", methods=['GET', 'POST'])
@login_required
def ricerca():
    return render_template('riparazioni/insert_riparazione.html', form=form)

@blueprint.route("/riparazioni_pendenti", methods=['GET'])
@login_required
def riparazioni_pendenti():
    riparazioni = Riparazione.query.filter_by(finito=False)
    return render_template("riparazioni/riparazioni_list.html", riparazioni=riparazioni.all())

@blueprint.route("/riparazioni_completate", methods=['GET'])
@login_required
def riparazioni_completate():
    riparazioni = Riparazione.query.filter_by(finito=True)
    return render_template("riparazioni/riparazioni_list.html", riparazioni=riparazioni.all())

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
