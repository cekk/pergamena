# -*- coding: utf-8 -*-
import datetime as dt

from flask.ext.login import UserMixin

from pergamena.extensions import bcrypt
from pergamena.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)


class Riparazione(SurrogatePK, Model):
    __tablename__ = 'riparazioni'
    cognome = Column(db.String(80), nullable=False)
    nome = Column(db.String(80), nullable=False)
    indirizzo = Column(db.String(80))
    citta = Column(db.String(80))
    telefono = Column(db.String(80))
    cell = Column(db.String(80))
    categoria = Column(db.String(80))
    oggetto = Column(db.String(80))
    descrizione = Column(db.Text, nullable=False)
    referenza = Column(db.String(80))
    peso = Column(db.Float)
    data_arrivo = Column(db.DateTime)
    consegna_prevista = Column(db.DateTime)
    difetto = Column(db.Text, nullable=False)
    riparatore = Column(db.String(80))
    n_riparazione = Column(db.String(80))
    preventivo = Column(db.Float)
    riparazione_effettuata = Column(db.Text)
    data_riparazione = Column(db.DateTime)
    garanzia = Column(db.String(80))
    costo_riparazione = Column(db.Float)
    spese_spedizione = Column(db.Float)
    totale = Column(db.Float)
    note = Column(db.Text)
    finito = Column(db.Boolean, default=False)


    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        return '<Riparazione({cognome} {nome})>'.format(cognome=self.cognome,
                                                        nome=self.nome)

class Categoria(SurrogatePK, Model):
    __tablename__ = 'categorie'
    nome = Column(db.String(80), nullable=False)

    def __init__(self, nome, **kwargs):
        db.Model.__init__(self, nome=nome, **kwargs)

    def __repr__(self):
        return '<Categoria({nome})>'.format(nome=self.nome)
