import csv, sqlite3

con = sqlite3.connect("Database.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
with open('GWAS.tsv','r') as fin:
    dr = csv.DictReader(fin, delimiter='\t')
    to_db = [(i['SNPS'], i['DATE'], i['LINK'], i['P-VALUE']) for i in dr]

cur.executemany("""
INSERT OR IGNORE INTO P_Value (
RS_ID, 
DATE_PUBLISHED,
LINK,
P_VALUE
)
VALUES
(?, ?, ?, ?) ;""", to_db,)
con.commit()
con.close()