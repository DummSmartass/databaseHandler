import pyodbc
import Fukcje
# Establish the connection
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=RPG;Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# SQL query
zapytanie = "select * from Racqe"

zapytanie = Fukcje.wypłaszcz(zapytanie)

try:
    cursor.execute(zapytanie)
    conn.commit()  # Commit the changes if the stored procedure modifies the data
except pyodbc.Error as e:
    sqlstate = e.args[1]
    if sqlstate == '01000':
        print("Warning: There was a warning from the database.")
    else:
        print(f"An error occurred: {e}")

cursor.close()
conn.close()
