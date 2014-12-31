# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, TextAreaField, BooleanField
from wtforms.fields.html5 import DateField, DecimalField
from wtforms.validators import DataRequired, EqualTo, Length, Optional

from .models import Riparazione

class InsertRiparazioneForm(Form):
    cognome = TextField('Cognome',
                    validators=[DataRequired()])
    nome = TextField('Nome',
                    validators=[DataRequired()])
    indirizzo = TextField('Indirizzo')
    citta = TextField(u'Città')
    telefono = TextField('Telefono')
    cell = TextField('Cellulare')
    categoria = TextField('Categoria',
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


class FinishRiparazioneForm(Form):
    riparazione_effettuata = TextAreaField('Riparazione effettuata')
    data_riparazione = DateField('Data della riparazione', validators=[Optional()])
    garanzia = TextField('Garanzia')
    costo_riparazione = DecimalField('Costo della riparazione', validators=[Optional()])
    spese_spedizione = DecimalField('Spese di spedizione', validators=[Optional()])
    totale = DecimalField('Totale', validators=[Optional()])
    note = TextAreaField('Note')
    finito = BooleanField('Finito')
