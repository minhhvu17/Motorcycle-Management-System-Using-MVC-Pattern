import mysql.connector
from db.settingup import SettingUp

"""
    This class is used to create a brand object
"""

class Brand:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="minhhvu11",
            database="motorbikemanagement",
            charset="utf8"
        )
        self.cursor = self.db.cursor()
        SettingUp()

    def add(self, name):
        response = 0
        # check if the brand is already in database
        self.cursor.execute("SELECT * FROM brand WHERE (Name = %s)", (name,))
        result = self.cursor.fetchall()
        if len(result) > 0:
            pass
        else:
            sql = "INSERT INTO Brand (Name) VALUES (%s)"
            self.cursor.execute(sql, (name,))
            self.db.commit()
            response = self.cursor.rowcount
        return response
        
    def delete(self, name):
        response = 0
        # check if the brand is already in database
        self.cursor.execute("SELECT * FROM brand WHERE (Name = %s)", (name,))
        result = self.cursor.fetchall()
        if len(result) == 0:
            pass
        else:
            sql = "DELETE FROM brand WHERE (Name = %s)"
            self.cursor.execute(sql, (name,))
            self.db.commit()
            response = self.cursor.rowcount
        return response
        
    def update(self, name, newName):
        response = 0
        # check if the brand is in database or not
        self.cursor.execute("SELECT * FROM brand WHERE (Name = %s)", (name,))
        result = self.cursor.fetchall()
        if len(result) == 0:
            pass
        else:
            sql = "UPDATE brand SET Name = %s WHERE Name = %s"
            self.cursor.execute(sql, (newName, name,))
            self.db.commit()
            response = self.cursor.rowcount
        return response
        
    def get(self, name):
        query = "SELECT * FROM brand WHERE name LIKE %s;"
        self.cursor.execute(query, ('%' + name + '%',))
        self.db.commit()
        result = self.cursor.fetchall()
        return result
    
    
    def get_brand_list(self):
        self.cursor.execute("select name, quantity from brand")
        result = self.cursor.fetchall()
        return result

    def check_add_brand(self, fields, brand_list):
        if fields.get() == '':
            return 0
        elif fields.get() in brand_list:
            return 1
        else:
            return 2
    
        
    def get_sum_brand(self):
        try:
            self.cursor.execute("select count(name) from brand")
            result = self.cursor.fetchall()
            result = result[0][0]
            return result
        except:
            return 0
    
    def sort(self, index):
        query = "select * from product order by " + index + ";"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    def filter(self, index):
        query = "select * from product where " + index + ";"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result