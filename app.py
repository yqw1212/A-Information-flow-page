#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')
from flask import Flask, render_template,  url_for, flash, redirect
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
import os,sys,click

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.debug = True
app.secret_key = 'neu'
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
'''
dev_db = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)
SQLALCHEMY_TRACK_MODIFICATIONS = False
'''
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class liuyan(FlaskForm):
    name = StringField('昵称', validators=[DataRequired(), Length(1, 20)])
    body = TextAreaField('留言', validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField()


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    timestamp2 = db.Column(db.DateTime, default=datetime.now, index=True)


#db.drop_all()
db.create_all()
@app.route('/', methods=['GET', 'POST'])
def index():
    form = liuyan()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Messages(body=body, name=name)
        db.session.add(message)
        db.session.commit()
        flash('Succeessful!')
        return redirect(url_for('index'))
    messages = Messages.query.order_by(Messages.timestamp.desc()).all()
    return render_template('index.html', form=form,messages=messages)


if __name__ == '__main__':
    app.run(debug=True)
