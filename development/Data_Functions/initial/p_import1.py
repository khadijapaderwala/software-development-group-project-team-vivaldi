import csv, sqlite3

con = sqlite3.connect("GWAS.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
#cur.execute("ALTER TABLE SNP ADD REGION")

with open('GWAS.tsv','r') as fin:
    dr = csv.DictReader(fin, delimiter='\t')
    to_db3 = [(i['REGION']) for i in dr]

cur.executemany("INSERT INTO SNP (REGION) VALUES (?);", to_db3)
con.commit()
con.close()