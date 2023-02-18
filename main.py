from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import sqlite3
import re
from markupsafe import escape

app = Flask(__name__)
# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAbSLAYALLDAY'


# Flask-Bootstrap requires this line
Bootstrap(app)


# Creating a search bar that user can input data into
class NameForm(FlaskForm):
    id = StringField('Please enter', validators=[DataRequired()])
    submit = SubmitField('Submit')

    
    
# Route to index page
@app.route('/', methods=['GET', 'POST']) # GET sends a webpage back, POST sends data entered to server
def index():
    form = NameForm()
    message = ""
    try:
        # If user searches through rs ID
        if form.validate_on_submit():
            id = form.id.data
            if id[:2] == 'rs':
                # empty the form field
                form.id.data = ""
                # redirect the browser to another route and template
                return redirect( url_for('SNPs', id=id) )
            
            # If user search through genomic position or genomic region
            elif id[:3] == 'chr':
                if id.find('-') != -1: # If string has a '-'
                    # Search id for characters starting with chr and ending in ':'
                    # .group(1) code calls on the characters between 'chr' and ':'
                    chr_n = (re.match('chr(.*):', id)).group(1)
                    # chr_p1 searches the position before the '-' and chr_p2 searches the position after the '-'
                    chr_p1 = (re.search(':(.*)-', id)).group(1)
                    chr_p2 = (re.search('-(.*)', id)).group(1)
                    form.id.data = ""
                    return redirect( url_for('Region_range', chr_n=chr_n, chr_p1=chr_p1, chr_p2=chr_p2) )
                # If user searches with 'chr' but string doesnt have an '-', single position is searched
                else:
                    chr_n = (re.match('chr(.*):', id)).group(1)
                    chr_p1 = (re.search(':(.*)', id)).group(1)
                    form.id.data = ""
                    return redirect( url_for('Region_single', chr_n=chr_n, chr_p1=chr_p1) )
                
            else:
                # Connect to database table called SNP_Gene
                conn = sqlite3.connect('Database/GWAS.db') 
                cur = conn.cursor()
                id = id.upper()
                cur.execute("SELECT Gene_ID FROM SNP_Gene WHERE Gene_ID=?", [id])
                rows = cur.fetchall()
                # If match isn't found then error message is returned
                if len(rows) == 0:
                    form.id.data = ""
                    message = """Hey, looks like you're searching something wild. 
                    Remember, if you're searching genomic coordinates please format it as 'chr[int]:[coordinate]-[coordinate]' or 'chr[int]:[coordinate]'. If you're searching for rs ID, please format it in lowercase.
                    Otherwise, it isn't in the database."""
                else:
                    return redirect(url_for('Gene', id=id))
                        
        return render_template('index.html', form=form, message=message)
    except Exception:
        form.id.data = ""
        message = """Hey, looks like you're searching something wild. 
                   Remember, if you're searching genomic coordinates please format it as 'chr[int]:[coordinate]-[coordinate]' or 'chr[int]:[coordinate]'. If you're searching for rs ID, please format it in lowercase.
                    Otherwise, it isn't in the database."""
        return render_template('index.html', form=form, message=message)

# Route to SNP page  
@app.route('/SNPs/<id>')
def SNPs(id):
    try:
        # Connect to database
        conn = sqlite3.connect('Database/GWAS.db') 
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
                    GROUP BY SNP.SNP_ID, SNP.P_value""", [id]) # Removes duplicate results
        rows = cur.fetchall()
        conn.close()
        if len(rows) == 0:
            return render_template('404.html', id=id) # If there are no results, 404 page will be rendered
        return render_template('SNP.html', id=id, rows=rows)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

# Route to region range page
@app.route('/Region/<chr_n>/<chr_p1>-<chr_p2>', methods=['GET', 'POST'])
def Region_range(chr_n, chr_p1, chr_p2):
    try:
        # Connect to database
        conn = sqlite3.connect('Database/GWAS.db')
        cur = conn.cursor()
        # Check select statement particularly joining through SNP_Gene
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
        #If not found in database render 404 template, otherwise return output
        if len(rows) == 0:
            return render_template('404.html', id=id)
        else:
            
            return render_template('Region.html', rows=rows, chr_n=chr_n, chr_p1=chr_p1, chr_p2=chr_p2) 
        
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
    
    
# Route to single region
@app.route('/Region/<chr_n>/<chr_p1>', methods=['GET', 'POST'])
def Region_single(chr_n, chr_p1):
    try:
        # Connect to database
        conn = sqlite3.connect('Database/GWAS.db')
        cur = conn.cursor()
        # Check select statement particularly joining through SNP_Gene
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
        # If not found in database, render 404 template, otherwise return output
        if len(rows) == 0:
            return render_template('404.html', id=id)
        else:
            return render_template('Region.html', rows=rows, chr_n=chr_n, chr_p1=chr_p1) #str(select)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
    
# Route to genes
@app.route('/Gene/<id>')
def Gene(id):
    try:
        # Connect to database
        conn = sqlite3.connect('Database/GWAS.db') 
        cur = conn.cursor()
        cur.execute("""SELECT SNP.SNP_ID, SNP.P_value as p_value, 
                    Region.CHR_ID as CHR, Region.CHR_pos as POS,
                    SNP_Gene.Gene_ID as GENE
                    FROM SNP_Gene
                    INNER JOIN Region ON Region.SNP_ID = SNP.SNP_ID
                    INNER JOIN SNP ON SNP.SNP_ID = SNP_Gene.SNP_ID
                    WHERE SNP_Gene.Gene_ID=?
                    GROUP BY SNP.SNP_ID, SNP.P_value""", [id]) # Removes duplicate results
        rows = cur.fetchall()
        conn.close()
        # If no results in database, 404 template will be rendered
        if len(rows) == 0:
            return render_template('404.html', id=id) 
        return render_template('Gene.html', id=id, rows=rows)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
        

if (__name__ == "__main__"):
    app.run(debug=True)
