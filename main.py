from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import sqlite3
import re
from markupsafe import escape

app = Flask(__name__)

### Creating a search bar
# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAbSLAYALLDAY'

# Flask-Bootstrap requires this line
Bootstrap(app)

class NameForm(FlaskForm):
    id = StringField('Please enter', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST']) #in addition to reading you also want to post from search bar
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    try:
        if form.validate_on_submit():
            id = form.id.data
            if id[:2] == 'rs':
                # empty the form field
                form.id.data = ""
                # redirect the browser to another route and template
                return redirect( url_for('SNPs', id=id) )
            elif id[:3] == 'chr':
                if id.find('-') != -1:
                    # match only  searches only from the beginning of the string and return match object if found. But if a match of substring is found somewhere in the middle of the string, it returns none. 
                    chr_n = (re.match('chr(.*):', id)).group(1)
                    # search searches for the whole string even if the string contains multi-lines and tries to find a match of the substring in all the lines of string.
                    chr_p1 = (re.search(':(.*)-', id)).group(1)
                    chr_p2 = (re.search('-(.*)', id)).group(1)
                    form.id.data = ""
                    return redirect( url_for('Region_range', chr_n=chr_n, chr_p1=chr_p1, chr_p2=chr_p2) )
                else:
                    chr_n = (re.match('chr(.*):', id)).group(1)
                    chr_p1 = (re.search(':(.*)', id)).group(1)
                    form.id.data = ""
                    return redirect( url_for('Region_single', chr_n=chr_n, chr_p1=chr_p1) )
            else:
                conn = sqlite3.connect('Database/GWAS.db') #connect to database
                cur = conn.cursor()
                id = id.upper()
                cur.execute("SELECT Gene_ID FROM SNP_Gene WHERE Gene_ID=?", [id])
                rows = cur.fetchall()
                if len(rows) == 0:
                    message = """Hey, looks like you're searching something wild. 
                    If you're searching genomic coordinates please format it as 'chr[int]:[coordinate]-[coordinate]' or 'chr[int]:[coordinate]'.
                    Otherwise, it ain't in the database."""
                else:
                    return redirect(url_for('Gene', id=id))
        return render_template('index.html', form=form, message=message)
    except Exception:
        message = """Hey, looks like you're searching something wild. 
        If you're searching genomic coordinates please format it as 'chr[int]:[coordinate]-[coordinate]' or 'chr[int]:[coordinate]'.
        Otherwise, it ain't in the database."""
        return render_template('index.html', form=form, message=message)

   
@app.route('/SNPs/<id>')
def SNPs(id):
    try:
        conn = sqlite3.connect('Database/GWAS.db') #connect to database
        cur = conn.cursor()
        cur.execute("""SELECT SNP.SNP_ID, SNP.P_value as p_value, 
                    Region.CHR_ID as CHR, Region.CHR_pos as POS,
                    SNP_Gene.Gene_ID as GENE,
                    CADD.CADD as CADD,
                    Context.Context as Context,
                    PopulationT.GBR_REF as GBRR, PopulationT.GBR_ALT as GBRA,
                    PopulationT.JPT_REF as JPTR, PopulationT.JPT_ALT as JPTA, 
                    PopulationT.ESN_REF as ESNR, PopulationT.ESN_ALT as ESNA
                    FROM SNP
                    INNER JOIN Region ON Region.SNP_ID = SNP.SNP_ID
                    INNER JOIN SNP_Gene ON SNP_Gene.SNP_ID = SNP.SNP_ID
                    INNER JOIN CADD ON CADD.SNP_ID = SNP.SNP_ID
                    INNER JOIN Context ON Context.Context_ID = SNP.SNP_ID
                    INNER JOIN PopulationT ON PopulationT.SNP_ID = SNP.SNP_ID
                    WHERE SNP.SNP_ID=?
                    GROUP BY SNP.SNP_ID, SNP.P_value""", [id]) ###removes duplicate results
        rows = cur.fetchall()
        print(rows)
        conn.close()
        if len(rows) == 0:
            return render_template('404.html', id=id) ### if there are no results, 404 page will be rendered
        return render_template('SNP.html', id=id, rows=rows)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route('/Region/<chr_n>/<chr_p1>-<chr_p2>', methods=['GET', 'POST'])
def Region_range(chr_n, chr_p1, chr_p2):
    try:
        conn = sqlite3.connect('Database/GWAS.db')
        cur = conn.cursor()
        #### check select statement particularly joining through snp_gene
        cur.execute("""SELECT SNP.SNP_ID, SNP.P_value as p_value, 
        Region.CHR_ID as CHR, Region.CHR_pos as POS,
        SNP_Gene.Gene_ID as GENE 
        FROM Region
        INNER JOIN SNP ON Region.SNP_ID = SNP.SNP_ID
        INNER JOIN SNP_Gene ON SNP.SNP_ID = SNP_Gene.SNP_ID
        WHERE CHR_ID=? 
        AND CHR_pos BETWEEN ? and ?
        GROUP BY SNP.SNP_ID, SNP.P_value;""", (chr_n, chr_p1, chr_p2))
        rows = cur.fetchall()
        conn.close()
        #select = request.form.get(row[0])
        if len(rows) == 0:
            return render_template('404.html', id=id)
        else:
            if request.method == 'POST':
                print(request.form.getlist('LD'))
                return 'Done'
        return render_template('Region.html', rows=rows, chr_n=chr_n, chr_p1=chr_p1, chr_p2=chr_p2) #str(select)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
    
@app.route('/Region/<chr_n>/<chr_p1>', methods=['GET', 'POST'])
def Region_single(chr_n, chr_p1):
    try:
        conn = sqlite3.connect('Database/GWAS.db')
        cur = conn.cursor()
        #### check select statement particularly joining through snp_gene
        cur.execute("""SELECT SNP.SNP_ID, SNP.P_value as p_value, 
        Region.CHR_ID as CHR, Region.CHR_pos as POS,
        SNP_Gene.Gene_ID as GENE 
        FROM Region
        INNER JOIN SNP ON Region.SNP_ID = SNP.SNP_ID
        INNER JOIN SNP_Gene ON SNP.SNP_ID = SNP_Gene.SNP_ID
        WHERE CHR_ID=? 
        AND CHR_pos=?
        GROUP BY SNP.SNP_ID, SNP.P_value;""", (chr_n, chr_p1))
        rows = cur.fetchall()
        conn.close()
        #select = request.form.get(row[0])
        if len(rows) == 0:
            return render_template('404.html', id=id)
        else:
            if request.method == 'POST':
                print(request.form.getlist('LD'))
                return 'Done'
        return render_template('Region.html', rows=rows, chr_n=chr_n, chr_p1=chr_p1) #str(select)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route('/Gene/<id>')
def Gene(id):
    try:
        conn = sqlite3.connect('Database/GWAS.db') #connect to database
        cur = conn.cursor()
        cur.execute("""SELECT SNP.SNP_ID, SNP.P_value as p_value, 
                    Region.CHR_ID as CHR, Region.CHR_pos as POS,
                    SNP_Gene.Gene_ID as GENE
                    FROM SNP_Gene
                    INNER JOIN Region ON Region.SNP_ID = SNP.SNP_ID
                    INNER JOIN SNP ON SNP.SNP_ID = SNP_Gene.SNP_ID
                    WHERE SNP_Gene.Gene_ID=?
                    GROUP BY SNP.SNP_ID, SNP.P_value""", [id]) ###removes duplicate results
        rows = cur.fetchall()
        conn.close()
        if len(rows) == 0:
            return render_template('404.html', id=id) ### if there are no results, 404 page will be rendered
        return render_template('Gene.html', id=id, rows=rows)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
        

if (__name__ == "__main__"):
    app.run(debug=True)