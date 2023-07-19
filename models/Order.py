import mysql.connector
from db.settingup import SettingUp

class Order:
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

    def add(self, fields):
        # add order to order table
        sql = "insert into orders (Date, Customer_Name, Customer_Phone, Model, Brand, Category, Color, price) values (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7],))
        self.db.commit()

        # update quantity in product table
        sql = "update product set quanity = quanity - 1 where name = %s"
        self.cursor.execute(sql, (fields[3],))
        self.db.commit()

        # update quantity in brand table
        sql = "update brand set quantity = quantity - 1 where name = %s"
        self.cursor.execute(sql, (fields[4],))
        self.db.commit()

        # update quantity in category table
        sql = "update category set quantity = quantity - 1 where name = %s"
        self.cursor.execute(sql, (fields[5],))
        self.db.commit()

    def get_product_list(self):
        self.cursor.execute("select name, brand, category, color, Selling_Price_M, quanity from product")
        result = self.cursor.fetchall()
        self.db.commit()
        return result
    
    def check_add_order(self,fields, order_list):
        for i in range(len(fields)):
            if fields[i].get() == "":
                return 0
            if fields[1].get().isdigit() == False:
                return 0
            
        for i in range(len(order_list)):
            if order_list[5] == 0:
                return -1
        return 1
    
    def get_order_list(self):
        self.cursor.execute("select Date, Customer_Name, Customer_Phone, Model, Brand, Category, Color, quantity, price from orders")
        result = self.cursor.fetchall()
        self.db.commit()
        return result
    
    def count_orders(self):
        try:
            self.cursor.execute("select count(*) from orders")
            result = self.cursor.fetchall()
            result = str(result[0][0])
            return result
        except:
            return "0"
    
    def total_price(self):
        try:
            self.cursor.execute("select sum(price) from orders")
            result = self.cursor.fetchall()
            # check if result > 1000 then change M to B
            if result[0][0] > 1000:
                # format result to 3 decimal places
                result = "{:.3f}".format(result[0][0]/1000) + " B"
            else:
                result = str(result[0][0]) + " M"
            self.db.commit()
            return result
        except:
            return "0 M"
        
    def delete_order(self, name):
        self.cursor.execute("delete from orders where Customer_Name = %s", (name,))
        self.db.commit()