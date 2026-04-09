import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from sqlalchemy.exc import IntegrityError
from archilog.data import get_all_money_pots, create_expense, delete_expense, delete_money_pot
from archilog.domain import get_money_pot_details
from archilog.forms import CreatePotForm, AddExpenseForm
from archilog.auth import auth

web_ui = Blueprint("web_ui", __name__)

@web_ui.route("/", methods=["GET"])
@auth.login_required
def home():
    pots = get_all_money_pots()
    form = CreatePotForm()
    return render_template("home.html", pots=pots, form=form)

@web_ui.route("/create_pot", methods=["POST"])
@auth.login_required(role="admin")
def create_pot():
    form = CreatePotForm()
    if form.validate_on_submit():
        pot_name = form.pot_name.data.strip()
        paid_by = form.paid_by.data.strip()
        amount = form.amount.data
        try:
            create_expense(pot_name, paid_by, amount)
            flash(f"Dépense de {amount}€ ajoutée pour {paid_by} dans '{pot_name}'.", "success")
            logging.info(f"Nouvelle cagnotte créée : {pot_name} par {paid_by}")
            return redirect(url_for('web_ui.pot_details', name=pot_name))
        except IntegrityError:
            flash(f"Impossible : {paid_by} a déjà payé pour la cagnotte '{pot_name}' !", "error")
            return redirect(url_for('web_ui.home'))

    pots = get_all_money_pots()
    return render_template("home.html", pots=pots, form=form)

# CORRECTION ICI : <name> au lieu de <n>
@web_ui.route("/pot/<name>", methods=["GET", "POST"])
@auth.login_required
def pot_details(name):
    form = AddExpenseForm()
    if form.validate_on_submit():
        paid_by = form.paid_by.data.strip()
        amount = form.amount.data
        try:
            create_expense(name, paid_by, amount)
            flash(f"Dépense de {amount}€ ajoutée pour {paid_by} !", "success")
        except IntegrityError:
            flash(f"Impossible : {paid_by} a déjà une dépense dans cette cagnotte !", "error")
        return redirect(url_for('web_ui.pot_details', name=name))

    try:
        mp, transactions = get_money_pot_details(name)
    except Exception:
        mp = None
        transactions = []
    return render_template("pot.html", name=name, mp=mp, transactions=transactions, form=form)

# CORRECTION ICI : <name> au lieu de <n>
@web_ui.route("/pot/<name>/delete", methods=["POST"])
@auth.login_required(role="admin")
def delete_expense_route(name):
    paid_by = request.form.get("paid_by")
    if paid_by:
        delete_expense(name, paid_by)
        flash(f"La dépense de {paid_by} a été supprimée.", "success")
    return redirect(url_for('web_ui.pot_details', name=name))

# CORRECTION ICI : <name> au lieu de <n>
@web_ui.route("/pot/<name>/delete_pot", methods=["POST"])
@auth.login_required(role="admin")
def delete_pot_route(name):
    delete_money_pot(name)
    flash(f"La cagnotte '{name}' a été supprimée.", "success")
    return redirect(url_for('web_ui.home'))

@web_ui.route("/test-500")
def test_error():
    abort(500)