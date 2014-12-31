# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from flask import Flask, render_template
from flask.ext.admin import Admin
from pergamena.settings import ProdConfig
from pergamena.assets import assets
from pergamena.extensions import (
    bcrypt,
    cache,
    db,
    login_manager,
    migrate,
    debug_toolbar,
)
from pergamena import public, user, riparazioni
from flask.ext.admin.contrib.sqla import ModelView
from pergamena.riparazioni.models import Riparazione, Categoria
from pergamena.user.models import User
from flask.ext.login import current_user


class AdminCategorie(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated()

    def __init__(self, session, **kwargs):
        super(AdminCategorie, self).__init__(Categoria, session, **kwargs)

class AdminRiparazioni(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated()

    def __init__(self, session, **kwargs):
        super(AdminRiparazioni, self).__init__(Riparazione, session, **kwargs)

class AdminUsers(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated()

    def __init__(self, session, **kwargs):
        super(AdminUsers, self).__init__(User, session, **kwargs)


def create_app(config_object=ProdConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_flaskadmin(app)
    return app


def register_flaskadmin(app):
    admin = Admin(app)
    admin.add_view(AdminUsers(db.session, name='Utenti'))
    admin.add_view(AdminCategorie(db.session, name='Categorie'))
    admin.add_view(AdminRiparazioni(db.session, name='Riparazioni'))
    return None


def register_extensions(app):
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(riparazioni.views.blueprint)
    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
