import sqlite3

class Client():
    def __init__(self,ID: int, name: str,budget: float):
        self.id = ID
        self.name = name
        self.budget = budget

    def create(self):
        cl =[(self.id,self.name,self.budget)]
        connection = sqlite3.connect('clients.db')
        cursor = connection.cursor()
        exist = cursor.execute("Select * FROM clients")
        print(exist)


        connection.commit()
        connection.close()
        return 0
    
    def read(self):
        connection = sqlite3.connect('clients.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM clients WHERE id=?;',(self.id,))
        print(cursor.fetchall())

        connection.commit()
        connection.close()
        return 
    
    def update(self):
        return 0
    
    def delete(self):
        return 0


