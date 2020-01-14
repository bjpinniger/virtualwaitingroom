from flask_wtf import FlaskForm
from wtforms.fields import  SelectField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Email


class VWR_Admin(FlaskForm):
    users = SelectField('User')
    tenants = SelectField('Department')
    submit = SubmitField()

class EnterEndpoint(FlaskForm):
    endpoint = StringField('Callback Address', validators=[DataRequired()], render_kw={'autofocus': True})
    callid = StringField('Call Id')
    tenant_id = StringField('Tenant Id')
    submit = SubmitField()

class Endpoint(FlaskForm):
    endpoint = StringField('Callback Address', validators=[DataRequired()], render_kw={'autofocus': True})
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Email()], render_kw={'autofocus': True})
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')