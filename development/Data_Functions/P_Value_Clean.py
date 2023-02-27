import sqlite3

con = sqlite3.connect("Database.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
### deletes all duplicate records. i.e. can have same rs IDs but different p-values but not the same p-values for the same rs IDs
cur.execute("""
DELETE FROM P_Value
WHERE EXISTS (
  SELECT 1 FROM P_Value p2 
  WHERE P_Value.P_VALUE = p2.P_VALUE
  AND P_Value.DATE_PUBLISHED = p2.DATE_PUBLISHED
  AND P_Value.LINK = p2.LINK
  AND P_Value.RS_ID = p2.RS_ID
  AND P_Value.rowid > p2.rowid
) ;""")
rows = cur.fetchall()
con.commit()
con.close()