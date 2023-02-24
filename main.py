from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import sqlite3
import re
from src.manhattan_plot import manhattan_plot
import pandas as pd
from src.creating_heatmap import LD, write_table_to_file, heatmap 

app = Flask(__name__)

### Creating a search bar
# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'vns66SX6SF6fa6FFHCB83SLAYALLDAY'

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
    error_msg= """Hey, looks like you're searching something wild. 
                    If you're searching genomic coordinates please format it as 'chr[int]:[coordinate]-[coordinate]' or 'chr[int]:[coordinate]'.
                    Otherwise, it ain't in the database."""
    try:
        if form.validate_on_submit():
            id = form.id.data
            if id[:2] == 'rs':
                # empty the form field
                form.id.data = ""
                # redirect the browser to another route and template
                return redirect( url_for('SNPs', id=id) )
            elif id[:3] == 'chr':
                if id.find('-') != -1 and id.find(':') != -1:
                    # match only  searches only from the beginning of the string and return match object if found. But if a match of substring is found somewhere in the middle of the string, it returns none. 
                    chr_n = (re.match('chr(.*):', id)).group(1)
                    # search searches for the whole string even if the string contains multi-lines and tries to find a match of the substring in all the lines of string.
                    chr_p1 = (re.search(':(.*)-', id)).group(1)
                    chr_p2 = (re.search('-(.*)', id)).group(1)
                    form.id.data = ""
                    if chr_n == '' or chr_p1 == '':
                        message = error_msg
                    else:
                        return redirect( url_for('Region_range', chr_n=chr_n, chr_p1=chr_p1, chr_p2=chr_p2) )
                else:
                    chr_n = (re.match('chr(.*):', id)).group(1)
                    chr_p1 = (re.search(':(.*)', id)).group(1)
                    form.id.data = ""
                    if chr_n == '' or chr_p1 == '':
                        message = error_msg
                    else:
                        return redirect( url_for('Region_single', chr_n=chr_n, chr_p1=chr_p1) )
            else:
                conn = sqlite3.connect('Database/Database.db') #connect to database
                cur = conn.cursor()
                id = id.upper()
                cur.execute("SELECT id FROM Gene WHERE id=?", [id])
                rows = cur.fetchall()
                if len(rows) == 0:
                    message = error_msg
                else:
                    return redirect(url_for('Gene', id=id))
        return render_template('index.html', form=form, message=message)
    except Exception:
        message = error_msg
        return render_template('index.html', form=form, message=message)

   
@app.route('/SNPs/<id>')
def SNPs(id):
    try:
        conn = sqlite3.connect('Database/Database.db') #connect to database
        cur = conn.cursor()
        cur.execute("""SELECT SNP.id, 
                    CHR_N, CHR_P,
                    REF_ALLELE, ALT_ALLELE,
                    GBR_REF_FREQ, GBR_ALT_FREQ,
                    JPT_REF_FREQ, JPT_ALT_FREQ,
                    ESN_REF_FREQ, ESN_ALT_FREQ,
                    CADD,
                    MIN(P_VALUE),
                    GENE.id, FUNCTIONAL
                    FROM SNP
                    INNER JOIN P_Value ON SNP.id = P_value.RS_ID
                    LEFT JOIN Gene_SNP ON SNP.id = Gene_SNP.SNP_ID
                    INNER JOIN Gene ON Gene.id = Gene_SNP.GENE_ID
                    JOIN Gene_Functions ON Gene.id = Gene_Functions.GENE_ID
                    WHERE SNP.id=?
                    GROUP BY Gene.id""", [id])
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
        conn = sqlite3.connect('Database/Database.db')
        cur = conn.cursor()
        #### check select statement particularly joining through snp_gene
        cur.execute("""SELECT SNP.id, 
        CHR_N, CHR_P,
        REF_ALLELE, ALT_ALLELE,
        GBR_REF_FREQ, GBR_ALT_FREQ,
        JPT_REF_FREQ, JPT_ALT_FREQ,
        ESN_REF_FREQ, ESN_ALT_FREQ,
        CADD,
        MIN(P_VALUE),
        GENE.id, FUNCTIONAL
        FROM SNP
        INNER JOIN P_Value ON SNP.id = P_value.RS_ID
        LEFT JOIN Gene_SNP ON SNP.id = Gene_SNP.SNP_ID
        INNER JOIN Gene ON Gene.id = Gene_SNP.GENE_ID
        JOIN Gene_Functions ON Gene.id = Gene_Functions.GENE_ID
        WHERE CHR_N=? 
        AND CHR_P BETWEEN ? and ?
        GROUP BY SNP.id, Gene.id
        ORDER BY CHR_P;""", (chr_n, chr_p1, chr_p2))
        rows = cur.fetchall()
        conn.close()
        form = NameForm()
        if form.validate_on_submit():
            id = form.id.data
            list_id = id.split(", ")
            print(list_id)
            data = LD(list_id)
            heat = heatmap(data, list_id)
            write_table_to_file(data)
            return redirect(url_for('txtfile'))

        #select = request.form.get(row[0])
        if len(rows) == 0:
            return render_template('404.html', id=id)
        else:
            #Create data frame for manhattan plot function
            rs_id = []
            p_value = []
            g_pos = []
            g_chron = []
            for i in rows:
                rs_id.append(i[0])
                p_value.append(i[12])
                g_pos.append(i[2])
                g_chron.append
            m_plots = {'CHR_POS':g_pos, 'P-VALUE':p_value}
            df = pd.DataFrame(m_plots)
            manhattan_plot(df, chr_n)
        return render_template('Region.html', rows=rows, chr_n=chr_n, chr_p1=chr_p1, chr_p2=chr_p2, form=form) #str(select)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
    
@app.route('/Region/<chr_n>/<chr_p1>', methods=['GET', 'POST'])
def Region_single(chr_n, chr_p1):
    try:
        conn = sqlite3.connect('Database/Database.db')
        cur = conn.cursor()
        #### check select statement particularly joining through snp_gene
        cur.execute("""SELECT SNP.id, 
        CHR_N, CHR_P,
        REF_ALLELE, ALT_ALLELE,
        GBR_REF_FREQ, GBR_ALT_FREQ,
        JPT_REF_FREQ, JPT_ALT_FREQ,
        ESN_REF_FREQ, ESN_ALT_FREQ,
        CADD,
        MIN(P_VALUE),
        GENE.id, FUNCTIONAL
        FROM SNP
        INNER JOIN P_Value ON SNP.id = P_value.RS_ID
        LEFT JOIN Gene_SNP ON SNP.id = Gene_SNP.SNP_ID
        INNER JOIN Gene ON Gene.id = Gene_SNP.GENE_ID
        JOIN Gene_Functions ON Gene.id = Gene_Functions.GENE_ID
        WHERE CHR_N=? 
        AND CHR_P=?
        GROUP BY SNP.id;""", (chr_n, chr_p1))
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
        conn = sqlite3.connect('Database/Database.db') #connect to database
        cur = conn.cursor()
        cur.execute("""SELECT SNP.id, 
        CHR_N, CHR_P,
        REF_ALLELE, ALT_ALLELE,
        GBR_REF_FREQ, GBR_ALT_FREQ,
        JPT_REF_FREQ, JPT_ALT_FREQ,
        ESN_REF_FREQ, ESN_ALT_FREQ,
        CADD,
        MIN(P_VALUE)
        FROM Gene
        LEFT JOIN Gene_SNP ON Gene.id = Gene_SNP.GENE_ID
        JOIN SNP ON SNP.id = Gene_SNP.SNP_ID
        INNER JOIN P_Value ON SNP.id = P_value.RS_ID 
        WHERE Gene.id = ?
        GROUP BY SNP.id
        """, [id]) ###removes duplicate results
        rows = cur.fetchall()

        cur.execute("SELECT FUNCTIONAL FROM Gene LEFT JOIN Gene_Functions ON Gene.id = Gene_Functions.GENE_ID WHERE id = ?", [id])
        func = cur.fetchall()
        print(func)

        conn.close()
        
        ### for selecting multiple RS for LD
        form = NameForm()
        if form.validate_on_submit():
            id = form.id.data
            list_id = id.split(", ")
            data = LD(list_id)
            write_table_to_file(data)
            return redirect(url_for('txtfile'))
        if len(rows) == 0:
            return render_template('404.html', id=id) ### if there are no results, 404 page will be rendered
        return render_template('Gene.html', id=id, rows=rows, func=func)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route('/LD')
def txtfile():
    return render_template('LD.html')
        

if (__name__ == "__main__"):
    app.run(debug=True)