import csv, sqlite3

con = sqlite3.connect("Database/GWAS.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
#cur.execute("ALTER TABLE REGION ADD SNPS")

with open('pathway_updated.txt','r') as fin:
    dr = csv.DictReader(fin, delimiter='\t')
    to_db = [(i['Variation IDs'], i['Description']) for i in dr]

cur.executemany(" INSERT INTO Context (Context_ID, Context) VALUES (?, ?);", to_db,)
con.commit()
con.close()