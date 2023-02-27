# Imported modules and functions
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


# Creates instance of flask application and assigns it to 'app'
app = Flask(__name__)


# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'vns66SX6SF6fa6FFHCB83SLAYALLDAY'

# Flask-Bootstrap requires this line
Bootstrap(app)

# Creates search bar on index page
class NameForm(FlaskForm):
    id = StringField('Please enter', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Creates search bar on the output pages
class LDForm(FlaskForm):
    ld = StringField('To calculate linkage disequilibrium, please enter (at least two) rs IDs separated by a comma.')
    search= SubmitField('Calculate')
    
    
# Route to index page
@app.route('/', methods=['GET', 'POST']) # GET sends a webpage back, POST sends data entered to server
def index():
    form = NameForm() # Assigns class to variable form
    message = ""
    error_msg= """Hey, looks like you're searching something wild. 
                    If you're searching genomic coordinates please format it as 'chr[int]:[coordinate]-[coordinate]' or 'chr[int]:                         [coordinate]'.
                    Otherwise, it ain't in the database."""
    try:
        # If user searches through rs ID by entering 'rs' as the first 2 letters
        if form.validate_on_submit():
            id = form.id.data
            if id[:2] == 'rs':
                form.id.data = "" # Empty Field
                # Redirect the browser to SNPs route
                return redirect( url_for('SNPs', id=id) )
            
            
             # If user search through genomic position or genomic region by entering 'chr' as the first 3 letters
            elif id[:3] == 'chr':
                if id.find('-') != -1 and id.find(':') != -1:
                   # If id has a '-'
                    # Search id for characters starting with chr and ending in ':'
                    # .group(1) code calls on the characters between 'chr' and ':'
                    chr_n = (re.match('chr(.*):', id)).group(1)
                     # chr_p1 searches the position before the '-' and chr_p2 searches the position after the '-'
                    chr_p1 = (re.search(':(.*)-', id)).group(1)
                    chr_p2 = (re.search('-(.*)', id)).group(1)
                    form.id.data = ""
                    # If not found then return error message, else return the route for Region_range
                    if chr_n == '' or chr_p1 == '':
                        message = error_msg
                    else:
                        return redirect( url_for('Region_range', chr_n=chr_n, chr_p1=chr_p1, chr_p2=chr_p2) )
                    
                    
                else:
                    # If user searches with 'chr' but id doesnt have an '-', route for Region_single is returned
                    chr_n = (re.match('chr(.*):', id)).group(1)
                    chr_p1 = (re.search(':(.*)', id)).group(1)
                    form.id.data = ""
                    if chr_n == '' or chr_p1 == '':
                        message = error_msg
                    else:
                        return redirect( url_for('Region_single', chr_n=chr_n, chr_p1=chr_p1) )
                    
                    
            else:
                conn = sqlite3.connect('Database/Database.db') # Connect to database
                cur = conn.cursor()
                id = id.upper() # Convert to uppercase
                cur.execute("SELECT id FROM Gene WHERE id=?", [id]) # Search in the Gene table in database
                rows = cur.fetchall()
                if len(rows) == 0: # If there is no match, return error message, else return route for Gene
                    message = error_msg
                else:
                    return redirect(url_for('Gene', id=id))
        return render_template('index.html', form=form, message=message)
    except Exception:
        message = error_msg
        return render_template('index.html', form=form, message=message)
    

# Route for SNPs   
@app.route('/SNPs/<id>', methods=['GET', 'POST'])
def SNPs(id):
    try:
        conn = sqlite3.connect('Database/Database.db') # Connect to database
        cur = conn.cursor()
        # Specifies column names from various tables and links tables together
        # WHERE SNP.id=? - specifies the condition that filters the rows 
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
        
        #LD search bar on the SNP output page
        form = LDForm()
        if form.validate_on_submit():
            ld = form.ld.data
            list_ld = ld.split(", ") # rs ids are split with a comma and put into a list
            print(list_ld)
            data = LD(list_ld)
            heat = heatmap(data, list_ld) # Using imported heat function to make a heatmap
            write_table_to_file(data)
            return redirect(url_for('txtfile')) # Return route for txtfile
        
        if len(rows) == 0:
            return render_template('404.html', id=id) # If there are no results, 404 page will be rendered
        return render_template('SNP.html', id=id, rows=rows, form=form) # If there are results, SNP.html template will be returned
    except Exception as e: # Error handling
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
    
    
#Route for Region_range
@app.route('/Region/<chr_n>/<chr_p1>-<chr_p2>', methods=['GET', 'POST'])
def Region_range(chr_n, chr_p1, chr_p2):
    try:
        conn = sqlite3.connect('Database/Database.db') # Connect to database
        cur = conn.cursor()
        # Specifies column names from various tables and links tables together
        # WHERE CHR_N=? - specifies the condition that filters the rows
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
        
        # LD search bar on the Region_range output page
        form = LDForm()
        if form.validate_on_submit():
            ld = form.ld.data
            list_ld = ld.split(", ") # rs ids are split with a comma and put into a list
            print(list_ld)
            data = LD(list_ld)
            heat = heatmap(data, list_ld) # Using imported heat function to make a heatmap
            write_table_to_file(data)
            return redirect(url_for('txtfile'))  # Return route for txtfile

        # If there are no results, the 404.html template will be rendered
        if len(rows) == 0:
            return render_template('404.html', id=id)
        # If variable rows isnt empty then manhattan plot is created and the Region.html template is returned
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
            # Imported function
            manhattan_plot(df, chr_n)
        return render_template('Region.html', rows=rows, chr_n=chr_n, chr_p1=chr_p1, chr_p2=chr_p2, form=form) 
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

# Route for Region_single     
@app.route('/Region/<chr_n>/<chr_p1>', methods=['GET', 'POST'])
def Region_single(chr_n, chr_p1):
    try:
        conn = sqlite3.connect('Database/Database.db') # Connect to database
        cur = conn.cursor()
        # Specifies column names from various tables and links tables together
        # WHERE CHR_N=? - specifies the condition that filters the rows
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
        
        # LD search bar on the Region_single output page
        form = LDForm()
        if form.validate_on_submit():
            ld = form.ld.data
            list_ld = ld.split(", ") # rs ids are split with a comma and put into a list
            print(list_ld)
            data = LD(list_ld)
            heat = heatmap(data, list_ld) # Using imported heat function to make a heatmap
            write_table_to_file(data)
            return redirect(url_for('txtfile')) # Return route for txtfile
        
        if len(rows) == 0:
            return render_template('404.html', id=id) #If there are no results, 404.html template is rendered, else region_single                                                              template is rendered
        return render_template('region_single.html', rows=rows, chr_n=chr_n, chr_p1=chr_p1, form=form) 
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


#Route for Gene
@app.route('/Gene/<id>', methods=['GET', 'POST'])
def Gene(id):
    try:
        conn = sqlite3.connect('Database/Database.db') # Connect to database
        cur = conn.cursor()
        # Specifies column names from various tables and links tables together
        # WHERE Gene.id=? - specifies the condition that filters the rows
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
        """, [id]) 
        rows = cur.fetchall()
        cur.execute("SELECT FUNCTIONAL FROM Gene LEFT JOIN Gene_Functions ON Gene.id = Gene_Functions.GENE_ID WHERE id = ?", [id])
        func = cur.fetchall()
        print(func)
        conn.close()
        
        # LD search bar on Gene output page
        form = LDForm()
        if form.validate_on_submit():
            ld = form.ld.data
            list_ld = ld.split(", ") # rs IDs split by a comma and put into a list
            print(list_ld)
            data = LD(list_ld)
            heat = heatmap(data, list_ld) # Imported heat function to create a heatmap
            write_table_to_file(data)
            return redirect(url_for('txtfile')) # Route for txtfile returned
        
        if len(rows) == 0:
            return render_template('404.html', id=id) # If there are no results, 404 page will be rendered
        return render_template('Gene.html', id=id, rows=rows, func=func, form=form) # Otherwsie Gene.html rendered
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

#Route for LD calculations
@app.route('/LD')
def txtfile():
    return render_template('LD.html') # LD.html rendered
        

# Run the application in debug mode
if (__name__ == "__main__"):
    app.run(debug=True)
