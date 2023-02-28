import csv, sqlite3
from sqlite3 import OperationalError


def executeScriptsFromFile(filename, cur):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            cur.execute(command)
        except OperationalError as msg:
            print("Command skipped: ", msg)

def main():
    con = sqlite3.connect("Database.db") # change to 'sqlite:///your_filename.db'
    cur = con.cursor()

    executeScriptsFromFile('Database.sql', cur) # connects to sql file which has the schema

# Allele Frequencies import by reading the file and inserting into table of SQL
    with open('Database/Datasets/Pop_Allele_Freq.csv','r') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['rsID'], i['REF'], i['ALT'], i['GBR_REF_FREQ'], i['GBR_ALT_FREQ'], i['JPT_REF_FREQ'], i['JPT_ALT_FREQ'], i['ESN_REF_FREQ'], i['ESN_ALT_FREQ']) for i in dr]

    cur.executemany("""INSERT OR IGNORE INTO SNP 
    (id, 
    REF_ALLELE, ALT_ALLELE, 
    GBR_REF_FREQ, GBR_ALT_FREQ, 
    JPT_REF_FREQ, JPT_ALT_FREQ,
    ESN_REF_FREQ, ESN_ALT_FREQ) 
    VALUES 
    (?, ?, ?,
    ?, ?, ?,
    ?, ?, ?);""", to_db,)

# CADD import
    with open('Database/Datasets/CADD_C6.csv','r') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['PHRED'], i['SNP']) for i in dr]

#As there's rs IDs in the SNP table, this will only add values to the specific rs ID
    cur.executemany("""
    UPDATE OR IGNORE SNP
    SET CADD = ?
    WHERE id = ? ;""", to_db,)

# Genomic Location for each SNP
    with open('Database/Datasets/GWAS.tsv','r') as fin:
        dr = csv.DictReader(fin, delimiter='\t')
        to_db = [(i['CHR_ID'], i['CHR_POS'], i['SNPS']) for i in dr]

    cur.executemany("""
    UPDATE SNP
    SET CHR_N = ?, CHR_P = ?
    WHERE
    id = ? ;""", to_db,)

# Needed another table for p-value as ther's multiple of them for one SNP
    with open('Database/Datasets/GWAS.tsv','r') as fin:
        dr = csv.DictReader(fin, delimiter='\t')
        to_db = [(i['SNPS'], i['DATE'], i['LINK'], i['P-VALUE'], i['PVALUE_MLOG']) for i in dr]

    cur.executemany("""
    INSERT OR IGNORE INTO P_Value (
    RS_ID, 
    DATE_PUBLISHED,
    LINK,
    P_VALUE,
    M_LOG
    )
    VALUES
    (?, ?, ?, ?, ?) ;""", to_db,)

#Remove duplicate records of same p-values with the same rs IDs
    cur.execute("""
    DELETE FROM P_Value
    WHERE EXISTS (
    SELECT 1 FROM P_Value p2 
    WHERE P_Value.P_VALUE = p2.P_VALUE
    AND P_Value.DATE_PUBLISHED = p2.DATE_PUBLISHED
    AND P_Value.LINK = p2.LINK
    AND P_Value.RS_ID = p2.RS_ID
    AND P_Value.M_LOG = p2.M_LOG
    AND P_Value.rowid > p2.rowid
    ) ;""")

#Gene with Functional Terms Import
    with open('Database/Datasets/Gene_Term_Updated.txt','r') as fin:
        dr = csv.DictReader(fin, delimiter='\t')
        to_db = [(i['Genes'], i['Function']) for i in dr]

        cur.executemany("""INSERT OR IGNORE INTO Gene 
        (id, FUNCTIONAL) 
        VALUES 
        (?, ?);""", to_db,)
    
#Gene with rs ID's
    with open('Database/Datasets/ensembl.txt','r') as fin:
        dr = csv.DictReader(fin, delimiter='\t')
        to_db = [(i['Symbol'], i['Variation ID']) for i in dr]

    cur.executemany("""INSERT OR IGNORE INTO Gene_SNP 
    (GENE_ID, SNP_ID) 
    VALUES 
    (?, ?);""", to_db,)

#Clean the rs IDs with gene IDs to remove duplicates
    cur.execute("""
    DELETE FROM Gene_SNP
    WHERE EXISTS (
    SELECT 1 FROM Gene_SNP p2 
    WHERE Gene_SNP.GENE_ID = p2.GENE_ID
    AND Gene_SNP.SNP_ID = p2.SNP_ID
    AND Gene_SNP.rowid > p2.rowid
    ) ;""")

    con.commit()
    con.close()

if __name__ == '__main__':
    main()