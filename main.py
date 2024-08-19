import sqlite3
import os
import datetime
import smtplib

class Report:
    def __init__(self):
        self.conn = sqlite3.connect('duedates.db')
        self.cursor = self.conn.cursor()
        self.today = datetime.date.today()

    def get_assignments(self):
        self.assignment_date = self.today + datetime.timedelta(days=5)
        self.assignments = self.cursor.execute('SELECT * FROM assignments WHERE due_date BETWEEN ? and ?', (self.today, self.today))
        return self.cursor.fetchall()

    def get_projects(self):
        self.project_date = self.today + datetime.timedelta(weeks=3)
        self.projects = self.cursor.execute('SELECT * FROM projects WHERE test_date BETWEEN ? and ?', (self.today, self.project_date))
        return self.cursor.fetchall()
    
    def get_tests(self):
        self.test_date = self.today + datetime.timedelta(weeks=2)
        self.tests = self.cursor.execute('SELECT * FROM tests WHERE test_date BETWEEN ? and ?', (self.today, self.test_date))
        return self.cursor.fetchall()
    
class Email:
    def __init__(self):
        self.email = os.environ.get('EMAIL')
        self.password = os.environ.get('PASSWORD')
        self.recipient = os.environ.get('RECIPIENT')
        self.subject = 'Upcoming Due Dates'
        self.message = ''

    def send_email(self, assignments, tests):
        self.message = f'Assignments due by {datetime.date.today() + datetime.timedelta(days=5)}:\n'
        for assignment in assignments:
            self.message += f'{assignment[0]}: {assignment[1]}\n'
        self.message += '\n'
        
        self.message += f'Tests due by {datetime.date.today() + datetime.timedelta(weeks=2)}:\n'
        for test in tests:
            self.message += f'{test[0]}: {test[1]}\n'
        
        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.email, self.password)
            smtp.sendmail(self.email, self.recipient, f'Subject: {self.subject}\n\n{self.message}')
    
if __name__ == '__main__':
    report = Report()
    email = Email()
    assignments = report.get_assignments()
    # projects = report.get_projects()
    tests = report.get_tests()
    email.send_email(assignments, tests)

    report.conn.close()