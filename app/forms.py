from flask_wtf import FlaskForm
from wtforms.fields import  SelectField, SubmitField, StringField, PasswordField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo


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
    username = StringField('Username', validators=[DataRequired()], render_kw={'autofocus': True})
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class AdminSettings(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

class Admin(FlaskForm):
    tenant = StringField('Tenant Name')
    tenants = SelectField('Tenants')
    create_tenant = SubmitField(label='Create Tenant')
    delete_tenant = SubmitField(label='Delete Tenant')
    create_guest_CLP = SubmitField(label='Create Guest CLP')
    create_host_CLP = SubmitField(label='Create Host CLP')
    spaces = SelectMultipleField('Orphaned Spaces')
    filter = StringField('Filter')
    delete_spaces = SubmitField(label='Delete Spaces')