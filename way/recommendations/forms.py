from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Text', validators=[DataRequired()])
    tag = RadioField('Tag', choices=[
        ('Extraversion', 'Extraversion'),
        ('Neuroticism', 'Neuroticism'),
        ('Agreeableness', 'Agreeableness'),
        ('Conscientiousness', 'Conscientiousness'),
        ('Openness', 'Openness')
    ])
    submit = SubmitField('Add Article')


class ResourceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Link', validators=[DataRequired()])
    tag = RadioField('Tag', choices=[
        ('Extraversion', 'Extraversion'),
        ('Neuroticism', 'Neuroticism'),
        ('Agreeableness', 'Agreeableness'),
        ('Conscientiousness', 'Conscientiousness'),
        ('Openness', 'Openness')
    ])
    submit = SubmitField('Add Resource')
