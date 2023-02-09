import csv, sqlite3

con = sqlite3.connect("GWAS.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
#cur.execute("ALTER TABLE REGION ADD SNPS")

with open('GWAS.tsv','r') as fin:
    dr = csv.DictReader(fin, delimiter='\t')
    to_db = [(i['REGION'], i['CHR_ID'], i['CHR_POS'], i['SNPS']) for i in dr]

cur.executemany("INSERT INTO REGION (REGION, CHR_ID, CHR_POS, SNP_ID) VALUES (?, ?, ?, ?);", to_db,)
con.commit()
con.close()