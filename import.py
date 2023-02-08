import csv, sqlite3

con = sqlite3.connect("GWAS.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
cur.execute("CREATE TABLE SNP (SNPS, PUBMEDID, P_VALUE, INTERGENIC);") # use your column names here
cur.execute("CREATE TABLE REGION (REGION, CHR_ID, CHR_POS);")

with open('GWAS.tsv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin, delimiter='\t') # comma is default delimiter
    to_db = [(i['SNPS'], i['PUBMEDID'], i['P-VALUE'], i['INTERGENIC']) for i in dr]
    to_db1 = [(i['REGION'], i['CHR_ID'], i['CHR_POS']) for i in dr]

cur.executemany("INSERT INTO SNP (SNPS, PUBMEDID, P_VALUE, INTERGENIC) VALUES (?, ?, ?, ?);", to_db)
cur.executemany("INSERT INTO REGION (REGION, CHR_ID, CHR_POS) VALUES (?, ?, ?);", to_db1)
con.commit()
con.close()