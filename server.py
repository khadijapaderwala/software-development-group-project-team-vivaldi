import os
from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, text
import sqlite3

app = Flask(__name__)

### Reading a database

db_name = 'GWAS.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# identify all columns by name and data type
class SNP(db.Model):
    __tablename__ = 'SNP'
    SNP_ID = db.Column(db.String, primary_key=True)
    Context_ID = db.Column(db.Integer)
    INTERGENIC = db.Column(db.Integer)
    P_VALUE = db.Column(db.Float),
    CADD = db.Column(db.Float)
    PUBMEDID = db.Column(db.Integer)


### Creating a search bar
# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAbSLAYALLDAY'

# Flask-Bootstrap requires this line
Bootstrap(app)

class NameForm(FlaskForm):
    id = StringField('Please enter a SNP', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        id = form.id.data
        if id[:2] == 'rs':
            # empty the form field
            form.id.data = ""
            # redirect the browser to another route and template
            return redirect( url_for('SNPs', id=id) )
        else:
            message = "That SNP rs's ID is not in our database."
    return render_template('index.html', form=form, message=message)
   
@app.route('/SNPs/<id>')
def SNPs(id):
    try:
        conn = sqlite3.connect('GWAS.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM SNP WHERE SNP_ID=?", [id])
        rows = cur.fetchall()
        conn.close()
        return render_template('SNP.html', id=id, rows=rows)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
        

if (__name__ == "__main__"):
    app.run(debug=True)