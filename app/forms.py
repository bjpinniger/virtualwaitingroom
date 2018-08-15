from flask_wtf import FlaskForm
from wtforms.fields import  SelectField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class SelectEndpoint(FlaskForm):
    endpoint = SelectField('Endpoint', validators=[DataRequired()])
    submit = SubmitField()