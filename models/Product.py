import mysql.connector
from db.settingup import SettingUp

"""
    This class is used to create a product object    
"""

class Product:
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

    # add a product to database include name, price, quantity, category
    def add(self, fields):
        response = 0
        for field in fields:
            if field.get() == "":
                return response
        # check if the product is already in database
        self.cursor.execute("select * from product where (Name = %s)", (fields[0].get(),))
        result = self.cursor.fetchall()
        self.db.commit()
        if result:
            pass
        else:
            sql = "insert into product (name, brand, category, length_mm, width_mm, height_mm, mass_kg, fuel_capacity_l, fuel_consumption_l_100km, engine_type, Maximize_Efficiency_kW_minute, color, Selling_Price_M, quanity) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (fields[0].get(), fields[1].get(), fields[2].get(), fields[3].get(), fields[4].get(), fields[5].get(), fields[6].get(), fields[7].get(), fields[8].get(), fields[9].get(), fields[10].get(), fields[11].get(), fields[12].get(), fields[13].get(),))
            self.db.commit()

            # brand_sql = "UPDATE Brand SET quantity = quantity + 1 WHERE (Name = %s)"
            # self.cursor.execute(brand_sql, (fields[1].get(),))
            # self.db.commit()

            # category_sql = "UPDATE Category SET quantity = quantity + 1 WHERE (Name = %s)"
            # self.cursor.execute(category_sql, (fields[2].get(),))
            # self.db.commit()

            brand_sql = "UPDATE Brand SET quantity = (SELECT SUM(quanity) FROM product WHERE (brand = %s)) WHERE (Name = %s)"
            self.cursor.execute(brand_sql, (fields[1].get(), fields[1].get(),))
            self.db.commit()

            category_sql = "UPDATE Category SET quantity = (SELECT SUM(quanity) FROM product WHERE (category = %s)) WHERE (Name = %s)"
            self.cursor.execute(category_sql, (fields[2].get(), fields[2].get(),))
            self.db.commit()

            response = self.cursor.rowcount
            self.db.commit()
        return response
    
    def delete(self, name):
        response = 0
        # check if the brand is already in database
        self.cursor.execute("SELECT * FROM product WHERE (Name = %s)", (name,))
        result = self.cursor.fetchall()
        if len(result) == 0:
            pass
        else:
            sql = "DELETE FROM product WHERE (Name = %s)"
            self.cursor.execute(sql, (name,))
            self.db.commit()
            response = self.cursor.rowcount
        return response
    
    def getName(self, name):
        query = "SELECT name, brand, category, length_mm, width_mm, height_mm, mass_kg, fuel_capacity_l, fuel_consumption_l_100km, engine_type, Maximize_Efficiency_kW_minute, color, Selling_Price_M, quanity FROM product WHERE name LIKE %s;"
        self.cursor.execute(query, ('%' + name + '%',))
        result = self.cursor.fetchall()
        self.db.commit()
        return result
    
    def get_brand_list(self):
        self.cursor.execute("select name, quantity from brand")
        result = self.cursor.fetchall()
        return result
    
    def get_sum_product(self):
        try:
            self.cursor.execute("select sum(quanity) from product")
            result = self.cursor.fetchall()
            result = str(result[0][0])
            return result
        except:
            return "0"
    
    def check_add_product(self,fields):
        for i in range(len(fields)):
            if fields[i].get() == "":
                return 0
        for field in fields:
            if field.get() == "":
                return 0
        self.cursor.execute("select * from product where (Name = %s)", (fields[0].get(),))
        result = self.cursor.fetchall()
        if result:
            return -1
        return 1
    
    def get_product_list(self):
        self.cursor.execute("select name, brand, category, length_mm, width_mm, height_mm, mass_kg, fuel_capacity_l, fuel_consumption_l_100km, engine_type, Maximize_Efficiency_kW_minute, color, Selling_Price_M, quanity from product")
        result = self.cursor.fetchall()
        self.db.commit()
        return result
    
    def delete_product(self, name):
        self.cursor.execute("select brand, category from product where (Name = %s)", (name,))
        result = self.cursor.fetchall()
        brand = result[0][0]
        category = result[0][1]
        print(brand, category)

        brand_sql = "UPDATE Brand SET quantity = quantity - 1 WHERE (Name = %s)"
        self.cursor.execute(brand_sql, (brand,))
        self.db.commit()

        category_sql = "UPDATE Category SET quantity = quantity - 1 WHERE (Name = %s)"
        self.cursor.execute(category_sql, (category,))
        self.db.commit()

        self.cursor.execute("delete from product where name = %s", (name,))
        self.db.commit()

    def update_product(self, fields, fields_old):
        response = 0
        # update product if it exists
        # check for other products except the one being updated
        # self.cursor.execute("SELECT * FROM product WHERE Name != %s", (fields_old[0],))
        # result = self.cursor.fetchall()
        # if not result:
        #     return response

        if fields[0] == fields_old[0]:
            self.cursor.execute("SELECT * FROM product WHERE Name != %s", (fields_old[0],))
            result = self.cursor.fetchall()
            if not result:
                return response
        else:            
            # check if the product is already in database
            self.cursor.execute("SELECT * FROM product WHERE Name = %s", (fields[0],))
            result = self.cursor.fetchall()
            if result:
                return response
            
        # update product information
        sql = """
            UPDATE product
            SET name = %s, brand = %s, category = %s, length_mm = %s, width_mm = %s, height_mm = %s,
                mass_kg = %s, fuel_capacity_l = %s, fuel_consumption_l_100km = %s, engine_type = %s,
                Maximize_Efficiency_kW_minute = %s, color = %s, Selling_Price_M = %s, quanity = %s
            WHERE Name = %s
        """
        self.cursor.execute(sql, (fields[0], fields[1], fields[2], fields[3],
                                fields[4], fields[5], fields[6], fields[7],
                                fields[8], fields[9], fields[10], fields[11],
                                fields[12], fields[13], fields_old[0]))
        self.db.commit()
        response = self.cursor.rowcount

        # after update, check if the brand and category are changed
        if fields[1] != fields_old[1]:
            # update brand quantity
            brand_sql = "UPDATE Brand SET quantity = quantity - 1 WHERE (Name = %s)"
            self.cursor.execute(brand_sql, (fields_old[1],))
            self.db.commit()

            brand_sql = "UPDATE Brand SET quantity = quantity + 1 WHERE (Name = %s)"
            self.cursor.execute(brand_sql, (fields[1],))
            self.db.commit()

        if fields[2] != fields_old[2]:
            # update category quantity
            category_sql = "UPDATE Category SET quantity = quantity - 1 WHERE (Name = %s)"
            self.cursor.execute(category_sql, (fields_old[2],))
            self.db.commit()

            category_sql = "UPDATE Category SET quantity = quantity + 1 WHERE (Name = %s)"
            self.cursor.execute(category_sql, (fields[2],))
            self.db.commit()

        return response
    
    def sort(self, index):
        query = "select name, brand, category, length_mm, width_mm, height_mm, mass_kg, fuel_capacity_l, fuel_consumption_l_100km, engine_type, Maximize_Efficiency_kW_minute, color, Selling_Price_M, quanity from product order by " + index + ";"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    def filter(self, index):
        query = "select name, brand, category, length_mm, width_mm, height_mm, mass_kg, fuel_capacity_l, fuel_consumption_l_100km, engine_type, Maximize_Efficiency_kW_minute, color, Selling_Price_M, quanity from product  order by " + index + ";"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    def filterBrand(self, name):
        query = "SELECT name, brand, category, length_mm, width_mm, height_mm, mass_kg, fuel_capacity_l, fuel_consumption_l_100km, engine_type, Maximize_Efficiency_kW_minute, color, Selling_Price_M, quanity FROM product WHERE Brand = %s;"
        self.cursor.execute(query, (name,))
        result = self.cursor.fetchall()
        self.db.commit()
        return result
    
    def filterCategory(self, name):
        query = "SELECT name, brand, category, length_mm, width_mm, height_mm, mass_kg, fuel_capacity_l, fuel_consumption_l_100km, engine_type, Maximize_Efficiency_kW_minute, color, Selling_Price_M, quanity FROM product WHERE Category = %s;"
        self.cursor.execute(query, (name,))
        result = self.cursor.fetchall()
        self.db.commit()
        return result
    
    # pass the name of the column and the type of sort
    def sortType(self, index, type):
        query = "select name, brand, category, length_mm, width_mm, height_mm, mass_kg, fuel_capacity_l, fuel_consumption_l_100km, engine_type, Maximize_Efficiency_kW_minute, color, Selling_Price_M, quanity from product order by " + index + " " + type + ";"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        print(result)
        return result   