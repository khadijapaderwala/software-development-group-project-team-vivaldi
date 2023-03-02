import csv, sqlite3

con = sqlite3.connect("Database.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
with open('CADD.csv','r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['CADD_PHRED'], i['SNP']) for i in dr]

cur.executemany("""
UPDATE OR IGNORE SNP
SET CADD = ?
WHERE id = ? ;""", to_db,)
con.commit()
con.close()