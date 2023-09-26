from tkinter import *
from client import Client
import sqlite3 

window = Tk()

client = Client(4,'Allfred',3)

client.create()




greeting = Label(text="Hello, Tkinter")
greeting.pack()


connection = sqlite3.connect('clients.db')
"""connection.execute('''CREATE TABLE clients(
ID INTIGER,
NAME TEXT,
BUDGET REAL
);''')
"""
cursor = connection.cursor()

cursor.execute('''
            SELECT * FROM clients
''')

print(cursor.fetchall())

connection.commit()
connection.close()

window.mainloop()