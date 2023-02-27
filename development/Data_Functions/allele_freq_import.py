import csv, sqlite3

con = sqlite3.connect("Database.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
with open('Pop_Allele_Freq.csv','r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['rsID'], i['REF'], i['ALT'], i['GBR_REF_FREQ'], i['GBR_ALT_FREQ'], i['JPT_REF_FREQ'], i['JPT_ALT_FREQ'], i['ESN_REF_FREQ'], i['ESN_ALT_FREQ']) for i in dr]

cur.executemany("""INSERT OR IGNORE INTO SNP 
(id, 
REF_ALLELE, ALT_ALLELE, 
GBR_REF_FREQ, GBR_ALT_FREQ, 
JPT_REF_FREQ, JPT_ALT_FREQ,
ESN_REF_FREQ, ESN_ALT_FREQ) 
VALUES 
(?, ?, ?,
?, ?, ?,
?, ?, ?);""", to_db,)
con.commit()
con.close()
#print(to_db[1][1]) just to see what it looks like