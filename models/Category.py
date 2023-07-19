import mysql.connector
from db.settingup import SettingUp

"""
    This class is used to create a category object
"""

class Category:
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
        # check if the category is already in database
        self.cursor.execute("SELECT * FROM category WHERE (Name = %s)", (name,))
        result = self.cursor.fetchall()
        if len(result) > 0:
            pass
        else:
            sql = "INSERT INTO category (Name) VALUES (%s)"
            self.cursor.execute(sql, (name,))
            self.db.commit()
            response = self.cursor.rowcount
        return response
        
    def delete(self, name):
        response = 0
        # check if the brand is already in database
        self.cursor.execute("SELECT * FROM category WHERE (Name = %s)", (name,))
        result = self.cursor.fetchall()
        if len(result) == 0:
            pass
        else:
            sql = "DELETE FROM category WHERE (Name = %s)"
            self.cursor.execute(sql, (name,))
            self.db.commit()
            response = self.cursor.rowcount
        return response
    
    def update(self, name, newName):
        response = 0
        # check if the brand is in database or not
        self.cursor.execute("SELECT * FROM category WHERE (Name = %s)", (name,))
        result = self.cursor.fetchall()
        if len(result) == 0:
            pass
        else:
            sql = "UPDATE category SET Name = %s WHERE Name = %s"
            self.cursor.execute(sql, (newName, name))
            self.db.commit()
            response = self.cursor.rowcount
        return response
    
    def get(self, name):
        query = "SELECT * FROM category WHERE name LIKE %s;"
        self.cursor.execute(query, ('%' + name + '%',))
        self.db.commit()
        result = self.cursor.fetchall()
        return result
    
    # def get_all(self):
    #     self.cursor.execute("SELECT * FROM category")
    #     result = self.cursor.fetchall()
    #     columns = [column[0] for column in self.cursor.description]  # get column names
    #     rows = []
    #     for row in result:
    #         row_dict = {}
    #         for i in range(len(columns)):
    #             row_dict[columns[i]] = row[i]
    #         rows.append(row_dict)
    #     return rows        
    
    def get_category_list(self):
        self.cursor.execute("select name, quantity from category")
        result = self.cursor.fetchall()
        return result
    
    def add_category(self, fields, category_list):
        if fields.get() == '' or fields.get() in category_list:
            return 0
        else:
            return 1
        
    def get_sum_category(self):
        self.cursor.execute("select count(name) from category")
        result = self.cursor.fetchall()
        result = result[0][0]
        return result