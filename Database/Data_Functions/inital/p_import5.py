import csv, sqlite3

con = sqlite3.connect("Database/GWAS.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS PopulationT ( 
SNP_ID text,
GBR_REF real, 
GBR_ALT real, 
JPT_REF real, 
JPT_ALT real, 
ESN_REF real, 
ESN_ALT real);""")

with open('Pop_Allele_Freq.csv','r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['rsID'], i['GBR_REF_FREQ'], i['GBR_ALT_FREQ'], i['JPT_REF_FREQ'], i['JPT_ALT_FREQ'], i['ESN_REF_FREQ'], i['ESN_ALT_FREQ']) for i in dr]

cur.executemany(" INSERT INTO PopulationT (SNP_ID, GBR_REF, GBR_ALT, JPT_REF, JPT_ALT, ESN_REF, ESN_ALT) VALUES (?, ?, ?, ?, ?, ?, ?);", to_db,)
con.commit()
con.close()