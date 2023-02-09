import csv, sqlite3

con = sqlite3.connect("GWAS.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()



#NEED A BETTER FUNCTION TO IMPORT DATA




with open('GWAS.tsv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin, delimiter='\t') # comma is default delimiter
    to_db = [(i['SNPS'], i['PUBMEDID'], i['P-VALUE'], i['INTERGENIC']) for i in dr]
    to_db1 = [(i['REGION'], i['CHR_ID'], i['CHR_POS'], i['SNPS']) for i in dr]

cur.executemany("INSERT INTO SNP (SNP_ID, PUBMEDID, P_VALUE, INTERGENIC) VALUES (?, ?, ?, ?);", to_db,)
cur.executemany("INSERT INTO REGION (REGION, CHR_ID, CHR_POS, SNP_ID) VALUES (?, ?, ?, ?);", to_db1,)
con.commit()
con.close()