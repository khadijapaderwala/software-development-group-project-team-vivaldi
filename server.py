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


### Creating a search bar
# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAbSLAYALLDAY'

# Flask-Bootstrap requires this line
Bootstrap(app)

class NameForm(FlaskForm):
    id = StringField('SNP name')
    gene = StringField('Gene name')
    pos= StringField('Genomic position')
    submit = SubmitField('Submit')
        
        
@app.route('/', methods=['GET', 'POST'])
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        id = form.id.data
        pos= form.pos.data
        gene= form.gene.data
        if id != "":
            # empty the form field
            form.id.data = ""
            # redirect the browser to another route and template
            return redirect( url_for('SNPs', id=id) )
        elif pos != "":
            form.pos.data= ""
            return redirect(url_for('position', pos=pos) )
        elif gene != "":
            form.gene.data= ""
            return redirect(url_for('gene', gene=gene) )
        else:
            message = "Not found, please enter something else"
    return render_template('index.html', form=form, message=message)


@app.route('/SNPs/<id>')
def SNPs(id):
    try:
        conn = sqlite3.connect('GWAS.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM SNP WHERE SNP_ID=?", [id]) #what database its looking for in SQL and what heading in                                                               data base it is looking at- this is how html template                                                            knows which rows and columns to select from the right database
        rows = cur.fetchall()
        conn.close()
        return render_template('SNP.html', id=id, rows=rows)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route('/position/<pos>')
def position(pos):
    try:
        conn = sqlite3.connect('GWAS.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM Region WHERE CHR_pos=?", [pos]) 
        rows = cur.fetchall()
        conn.close()
        return render_template('position.html', pos=pos, rows=rows)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route('/gene/<gene>')
def gene(gene):
    try:
        conn = sqlite3.connect('GWAS.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM Gene WHERE Gene_ID=?", [gene]) 
        rows = cur.fetchall()
        conn.close()
        return render_template('gene.html', gene=gene, rows=rows)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
    
if (__name__ == "__main__"):
    app.run(debug=True)
