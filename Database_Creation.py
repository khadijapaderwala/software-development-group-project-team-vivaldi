import sqlite3
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
    con = sqlite3.connect("GWAS.db") # change to 'sqlite:///your_filename.db'
    cur = con.cursor()

    executeScriptsFromFile('schema.sql', cur)

    con.close()

if __name__ == '__main__':
    main()