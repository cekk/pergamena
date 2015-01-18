# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_user, login_required, logout_user, current_user

from pergamena.extensions import login_manager
from pergamena.user.models import User
from pergamena.public.forms import LoginForm
from pergamena.user.forms import RegisterForm
from pergamena.utils import flash_errors
from pergamena.database import db
from pergamena.riparazioni.models import Riparazione

blueprint = Blueprint('public', __name__, static_folder="../static")

@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = LoginForm(request.form)
    riparazioni_pendenti = 0
    riparazioni_completate = 0
    if current_user.is_authenticated():
        riparazioni_pendenti = Riparazione.query.filter_by(finito=False).count()
        riparazioni_completate = Riparazione.query.filter_by(finito=True).count()
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash("Ti sei loggato.", 'success')
            redirect_url = request.args.get("next") or url_for("public.home")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html",
                           form=form,
                           riparazioni_pendenti=riparazioni_pendenti,
                           riparazioni_completate=riparazioni_completate)

@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('Ti sei disconnesso.', 'info')
    return redirect(url_for('public.home'))

@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User.create(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data,
                        active=True)
        flash("Grazie per la registrazione. Adesso puoi effettuare il log in.", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)
