from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class CreatePotForm(FlaskForm):
    pot_name = StringField('Nom de la cagnotte', validators=[DataRequired(message="Le nom de la cagnotte est requis.")])
    paid_by = StringField('Payé par', validators=[DataRequired(message="Le nom du participant est requis.")])
    amount = FloatField('Montant', validators=[
        DataRequired(message="Le montant est requis."),
        NumberRange(min=0.01, message="Le montant doit être supérieur à 0.")
    ])
    submit = SubmitField('Ajouter')

class AddExpenseForm(FlaskForm):
    paid_by = StringField('Payé par', validators=[DataRequired(message="Le nom du participant est requis.")])
    amount = FloatField('Montant', validators=[
        DataRequired(message="Le montant est requis."),
        NumberRange(min=0.01, message="Le montant doit être supérieur à 0.")
    ])
    submit = SubmitField('Ajouter')