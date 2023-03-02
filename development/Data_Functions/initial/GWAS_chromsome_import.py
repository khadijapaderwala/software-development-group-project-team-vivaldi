import csv, sqlite3

con = sqlite3.connect("Database.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
with open('GWAS.tsv','r') as fin:
    dr = csv.DictReader(fin, delimiter='\t')
    to_db = [(i['CHR_ID'], i['CHR_POS'], i['SNPS']) for i in dr]

cur.executemany("""
UPDATE SNP
SET CHR_N = ?, CHR_P = ?
WHERE
id = ? ;""", to_db,)
con.commit()
con.close()