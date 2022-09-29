from flask_wtf import FlaskForm
from wtforms import IntegerField,SubmitField,TextField,FloatField,BooleanField,StringField,SelectField,Form
from wtforms.validators import DataRequired,InputRequired


class AlgoForm(FlaskForm):
    amlitude = FloatField('Amlitude',validators=[DataRequired()])
    RR = FloatField('RR',validators=[DataRequired()])
    speed = FloatField('Speed',validators=[DataRequired()])
    Age = IntegerField('Age',validators=[DataRequired()])
    Sex = SelectField('Sex',choices = ['MALE','FEMALE'],validators=[DataRequired()])
    Medicine = SelectField('Medicine',choices = ['Yes','No'],validators=[DataRequired()])
    submit = SubmitField('Predict')