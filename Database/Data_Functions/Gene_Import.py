import csv, sqlite3

con = sqlite3.connect("Database.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
with open('pathway_updated.txt','r') as fin:
    dr = csv.DictReader(fin, delimiter='\t')
    to_db = [(i['Genes Involved'], i['Description']) for i in dr]

cur.executemany("""INSERT OR IGNORE INTO Gene_Functions 
(GENE, FUNCTIONAL) 
VALUES 
(?, ?);""", to_db,)
con.commit()
con.close()