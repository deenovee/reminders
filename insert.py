import csv
import sqlite3
from datetime import datetime

def insert_data():
    conn = sqlite3.connect('duedates.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS assignments (
                        assignment_name TEXT,
                        due_date TEXT
                      )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS tests (
                        test_name TEXT,
                        test_date TEXT
                      )''')

    # Function to convert date strings from "1/1/24" to the correct format
    def convert_date(date_str):
        return datetime.strptime(date_str, "%m/%d/%y").strftime("%Y-%m-%d")
    
    # Insert data into assignments table
    with open('homework.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            row[1] = convert_date(row[1].strip())  # Convert the date string in the second column
            cursor.execute('INSERT INTO assignments VALUES (?, ?)', row)
    
    # Insert data into tests table
    with open('tests.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            row[1] = convert_date(row[1].strip())  # Convert the date string in the second column
            cursor.execute('INSERT INTO tests VALUES (?, ?)', row)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    insert_data()
