import csv, sqlite3

con = sqlite3.connect("Database.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS Gene (
	M_GENE text PRIMARY KEY,
	ONTOL text
);""")
with open('pathway_updated.txt','r') as fin:
    dr = csv.DictReader(fin, delimiter='\t')
    to_db = [(i['Genes Involved'], i['Parent(s)']) for i in dr]

cur.executemany("""INSERT OR IGNORE INTO Gene 
(M_GENE, ONTOL) 
VALUES 
(?, ?);""", to_db,)
con.commit()
con.close()