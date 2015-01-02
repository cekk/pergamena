# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, TextAreaField, BooleanField
from wtforms.fields.html5 import DateField, DecimalField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, EqualTo, Length, Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .models import Riparazione, Categoria


def available_categories():
    return Categoria.query.order_by('nome')


class InsertRiparazioneForm(Form):
    cognome = TextField('Cognome',
                    validators=[DataRequired()])
    nome = TextField('Nome',
                    validators=[DataRequired()])
    indirizzo = TextField('Indirizzo')
    citta = TextField(u'Città')
    telefono = TextField('Telefono')
    cell = TextField('Cellulare')
    categoria = QuerySelectField('Categoria',
                    query_factory=available_categories,
                    blank_text=u'-- seleziona --',
                    allow_blank=True,
                    get_label='nome',
                    validators=[DataRequired()])
    oggetto = TextField('Oggetto')
    descrizione = TextAreaField('Descrizione',
                    validators=[DataRequired()])
    referenza = TextField('Referenza')
    peso = DecimalField('Peso', validators=[Optional()])
    data_arrivo = DateField('Data di arrivo', validators=[Optional()])
    consegna_prevista = DateField('Data di consegna prevista', validators=[Optional()])
    difetto = TextAreaField('Difetto')
    riparatore = TextField('Riparatore')
    n_riparazione = TextField('Numero riparatore')
    preventivo = DecimalField('Preventivo', validators=[Optional()])


class CompletaRiparazioneForm(InsertRiparazioneForm):
    riparazione_effettuata = TextAreaField('Riparazione effettuata')
    data_riparazione = DateField('Data della riparazione', validators=[Optional()])
    garanzia = TextField('Garanzia')
    costo_riparazione = DecimalField('Costo della riparazione', validators=[Optional()])
    spese_spedizione = DecimalField('Spese di spedizione', validators=[Optional()])
    totale = DecimalField('Totale', validators=[Optional()])
    note = TextAreaField('Note')


class ImportDb(Form):
    file = FileField('File')
