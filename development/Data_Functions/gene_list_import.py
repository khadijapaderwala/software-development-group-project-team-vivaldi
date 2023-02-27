import csv, sqlite3

con = sqlite3.connect("Database.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
with open('Database/Datasets/Gene.txt','r') as fin:
        dr = csv.DictReader(fin, delimiter='\t')
        to_db = [(i['Genes'],) for i in dr]


      
cur.executemany("""INSERT INTO Gene(id)
        VALUES (?);""", to_db)

con.commit()
con.close()