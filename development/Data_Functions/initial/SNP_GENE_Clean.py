import sqlite3

con = sqlite3.connect("Database/Database.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
### deletes all duplicate records. i.e. can have same rs IDs but different p-values but not the same p-values for the same rs IDs
cur.execute("""
SELECT * FROM Gene_SNP
WHERE EXISTS (
  SELECT 1 FROM Gene_SNP p2 
  WHERE Gene_SNP.GENE_ID = p2.GENE_ID
  AND Gene_SNP.SNP_ID = p2.SNP_ID
  AND Gene_SNP.rowid > p2.rowid
) ;""")
rows = cur.fetchall()
print(rows)
con.commit()
con.close()