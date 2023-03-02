import csv, sqlite3

con = sqlite3.connect("Database/GWAS.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS CADD (
    SNP_ID text,
	Consequence text,
    CADD real);""")

with open('CADD.csv','r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['SNP'], i['Consequence'], i['CADD_PHRED']) for i in dr]

cur.executemany(" INSERT INTO CADD (SNP_ID, Consequence, CADD) VALUES (?, ?, ?);", to_db,)
con.commit()
con.close()