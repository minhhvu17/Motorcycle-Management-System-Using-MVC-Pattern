from core.Controller import Controller
from core.Core import Core
from models.Product import Product
from tkinter import messagebox
from models.Brand import Brand
from models.Category import Category
import tkinter as tk
from tkinter import ttk
from views.EditView import EditView as EditView
from models.Order import Order
import time

"""
    Main controller. It will be responsible for program's main screen behavior.
"""
class HomeController(Controller):
    #-----------------------------------------------------------------------
    #        Constructor
    #-----------------------------------------------------------------------
    def __init__(self,root):
        self.homeView = self.loadView("Home",root)
        self.reverse = False
        #self.brand = Brand()
    
    #-----------------------------------------------------------------------
    #        Methods
    #-----------------------------------------------------------------------
    product = Product()
    brand = Brand()
    category = Category()
    order = Order()

# ----------------------------------------------------------------
    def on_tree_select(self, event, tree, productEntry):
        # Get the id of the selected row
        item = event.widget.selection()[0]
        # Get the values of the selected row
        values = tree.item(item, "values")
        # Store the values in a class variable
        productEntry.configure(state="normal")
        productEntry.delete(0, "end")
        productEntry.insert(0, values[0])
        productEntry.configure(state="disabled")
        # return productInput
        # self.order_list_box(temp_frame, values)

        # Select item, double click to edit
    def on_select(self, event):
        selected_item = None
        if len(event.widget.selection()) > 0:
            selected_item = event.widget.selection()[0]
            
        # perform some action with the selected item
        if selected_item is not None:
            selected_item = event.widget.selection()[0]
            values = event.widget.item(selected_item)['values']
            edit_view = self.loadEdit("edit",tk.Tk(), values, self.frame)
            # reset selected item
            event.widget.selection_remove(selected_item)
        # edit_view.showEditView(values)

    # Delete item, press delete button to delete
    def on_delete(self, event):    
        selected_items = event.widget.selection()    
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected item(s)?")
        if confirm:        
            for item in selected_items:            
                item_values = event.widget.item(item, "values")            
                self.product.delete_product(item_values[0])            
                event.widget.delete(item)

    def order_delete(self, event):
        selected_items = event.widget.selection()
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected item(s)?")
        if confirm:
            for item in selected_items:
                item_values = event.widget.item(item, "values")
                self.order.delete_order(item_values[1])
                event.widget.delete(item)



#DASHBOARD
    def get_sum_product(self):
        return str(self.product.get_sum_product())
    def get_sum_brand(self):
        return str(self.brand.get_sum_brand())
    def get_sum_soldproduct(self):
        return str(self.order.count_orders())
    def get_profit(self):
        return str(self.order.total_price())
    

    

#ADD_BRAND    
    def btnAdd_Brand(self,entry, tree, contentFrame):
        brand_name_list = []
        brand = self.brand.get_brand_list()
        for i in range(len(brand)):
            brand_name_list.append(brand[i][0])
        response = self.brand.check_add_brand(entry, brand_name_list)
        if response > 1:           
            messagebox.showinfo("Add brand", "Brand successfully added!")
            brand_name = entry.get()
            self.brand.add(brand_name)
        elif response == 0:
            messagebox.showerror("Add brand", "Error while adding brand!")
        else: 
            messagebox.showerror("Add brand", "Brand already exists!")
        entry.delete(0, 'end')
        self.reset_BrandList(tree, contentFrame)

#DISPLAY_BRAND_LIST
    def showTreeView_BrandList(self, contentFrame):
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        tree = ttk.Treeview(contentFrame, height=11)
        tree["columns"] = ("brand", "quantity")
        tree.column("#0", width=150, stretch=False, anchor="center")
        tree.column("brand", width=600, stretch=False, anchor="center")
        tree.column("quantity", width=200, stretch=False, anchor="center")
        tree.heading("#0", text="No.", anchor="center")
        tree.heading("brand", text="Brand", anchor="center")
        tree.heading("quantity", text="Quantity", anchor="center")
        tree.place(x= 20, y = 160, width = 970, height = 440)
        brand_list = self.product.get_brand_list()
        for i in range(len(brand_list)):
            tree.insert('', 'end', text=i+1, values=(brand_list[i][0], brand_list[i][1]))
        # Scrollbar
        scrollBar = ttk.Scrollbar(contentFrame, orient="vertical", command=tree.yview)
        scrollBar.place(x=970, y=160, height=440, width = 20)
        tree.configure(yscrollcommand=scrollBar.set)
        return tree
    
    def reset_BrandList(self, tree, contentFrame):
        tree.destroy()
        tree = self.showTreeView_BrandList(contentFrame)

    def BrandList_added(self, brand_list, brand):
        brand_list.append(brand)
        return brand_list
    
    def get_brand_list_added(self):
        brand_list = self.brand.get_brand_list()
        return brand_list   

    
    
    
    
    #PRODUCT :
    def btnAdd_Product(self, fields):
        product = []
        response = self.product.check_add_product(fields)
        if response == -1:
            messagebox.showerror("Add brand", "Product already exists!")
            pass
        if response > 0:           
            messagebox.showinfo("Add brand", "Product successfully added!")
            for i in range(len(fields)):
                product.append(fields[i].get())
            self.product.add(fields)
            pass
        elif response == -1:
            messagebox.showerror("Add brand", "Product already exists!")
            pass
        else: 
            messagebox.showerror("Add brand", "Some fields are empty or wrong type!")
            pass
        for i in range(len(fields)):
            fields[i].delete = (0, 'end')

    def clearContent(self, fields):
        for i in range(len(fields)):
            fields[i].delete = (0, 'end')           

    def reset_ProductList(self, tree, product_list, contentFrame):
        tree.destroy()
        tree = self.showTreeView_ProductList(contentFrame, product_list)  

    def btnUpdate_Product(self, fields, fields_old,frame, contentFrame):
        # use update_product function from product class
        for i in range(len(fields)):
            fields[i] =  fields[i].get()
        response = self.product.update_product(fields, fields_old)
        if response == 1:
            messagebox.showinfo("Success", "Update product successfully")
            self.tree1.destroy()
            self.showTreeView_ProductList(contentFrame, self.searchContent, self.filterContent, self.categoryContent, self.brandContent)
            frame.destroy()
        else:
            messagebox.showerror("Error", "Update product failed")
        

    def showTreeView_ProductList(self, contentFrame, productFrame, searchContent, filterContent, categoryContent, brandContent):
        self.frame = contentFrame
        self.searchContent = searchContent
        self.filterContent = filterContent
        self.categoryContent = categoryContent
        self.brandContent = brandContent
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        tree = ttk.Treeview(productFrame, height=11)
        tree["columns"] = ("Name", "brand", "category", "length_mm", "width_mm", "height_mm", "mass_kg", "fuel_capacity", "fuel_consumption_100km", "engine_type", "Maximize_Efficiency_kW_minute", "color", "Selling_Price_M", "quantity" )
        tree.column("#0", width=50, stretch=False, anchor="center")
        tree.column("Name", width=250, stretch=False, anchor="center")
        tree.column("brand", width=100, stretch=False, anchor="center")
        tree.column("category", width=100, stretch=False, anchor="center")
        tree.column("length_mm", width=100, stretch=False, anchor="center")
        tree.column("width_mm", width=100, stretch=False, anchor="center")
        tree.column("height_mm", width=100, stretch=False, anchor="center")
        tree.column("mass_kg", width=100, stretch=False, anchor="center")
        tree.column("fuel_capacity", width=200, stretch=False, anchor="center")
        tree.column("fuel_consumption_100km", width=200, stretch=False, anchor="center")
        tree.column("engine_type", width=140, stretch=False, anchor="center")
        tree.column("Maximize_Efficiency_kW_minute", width=140, stretch=False, anchor="center")
        tree.column("color", width=140, stretch=False, anchor="center")
        tree.column("Selling_Price_M", width=140, stretch=False, anchor="center")
        tree.column("quantity", width=0, stretch=False, anchor="center")
        tree.heading("#0", text="No.", anchor="center")
        tree.heading("Name", text="Name", anchor="center")
        tree.heading("brand", text="Brand", anchor="center")
        tree.heading("category", text="Category", anchor="center")
        tree.heading("length_mm", text="Length (mm)", anchor="center")
        tree.heading("width_mm", text="Width (mm)", anchor="center")
        tree.heading("height_mm", text="Height (mm)", anchor="center")
        tree.heading("mass_kg", text="Mass (kg)", anchor="center")
        tree.heading("fuel_capacity", text="Fuel Capacity (L)", anchor="center")
        tree.heading("fuel_consumption_100km", text="Fuel Consumption (100km)", anchor="center")
        tree.heading("engine_type", text="Engine Type", anchor="center")
        tree.heading("Maximize_Efficiency_kW_minute", text="Maximize Efficiency (kW/minute)", anchor="center")
        tree.heading("color", text="Color", anchor="center")
        tree.heading("Selling_Price_M", text="Selling Price (M)", anchor="center")
        tree.heading("quantity", text="Quantity", anchor="center")
        tree.place(x= 0, y = 0, width = 1000, height = 450)
        product_list = self.product.get_product_list()
        # product_list_filter = product_list.copy()
        if categoryContent != 'Category':
            product_list_by_category = self.product.filterCategory(categoryContent)
        else:
            product_list_by_category = product_list
            
        if brandContent != 'Brand':
            product_list_by_brand = self.product.filterBrand(brandContent)
        else:
            product_list_by_brand = product_list
        
        product_list_by_category_brand = []
        for i in product_list_by_category:
            if i in product_list_by_brand:
                product_list_by_category_brand.append(i)
        
        if filterContent != 'Sort':
            product_list_filter = self.product.filter(filterContent)
        else:
            product_list_filter = product_list
        
        displayList = []
        for i in product_list_filter:
            if i in product_list_by_category_brand:
                displayList.append(i)
        if searchContent == '':
            for i in range(len(displayList)):
                tree.insert('', 'end', text=i+1, values=(displayList[i][0], displayList[i][1], displayList[i][2], displayList[i][3], displayList[i][4], displayList[i][5], displayList[i][6], displayList[i][7], displayList[i][8], displayList[i][9], displayList[i][10], displayList[i][11], displayList[i][12], displayList[i][13]))
        else: 
            for i in range(len(displayList)):
                if searchContent.lower() in displayList[i][0].lower():
                    tree.insert('', 'end', text=i+1, values=(displayList[i][0], displayList[i][1], displayList[i][2], displayList[i][3], displayList[i][4], displayList[i][5], displayList[i][6], displayList[i][7], displayList[i][8], displayList[i][9], displayList[i][10], displayList[i][11], displayList[i][12], displayList[i][13]))

        tree.bind("<Double-1>", self.on_select)
        tree.bind("<Delete>", self.on_delete)

        # Scrollbar
        scrollBarY = ttk.Scrollbar(contentFrame, orient="vertical", command=tree.yview)
        scrollBarY.place(x=990, y=160, height=440, width = 20)
        tree.configure(yscrollcommand=scrollBarY.set)
        scrollBarX = ttk.Scrollbar(contentFrame, orient="horizontal", command=tree.xview)
        scrollBarX.place(x=20, y=600, height=20, width = 970)
        tree.configure(xscrollcommand=scrollBarX.set)
        self.tree1 = tree
        return tree
    




    # ORDER LIST
    def showTreeView_OrderProductList(self, contentFrame, productEntry):
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        tree = ttk.Treeview(contentFrame, height=11)
        tree["columns"] = ("product", "brand", "category", "color", "Selling_Price_M", "quantity")
        tree.column("#0", width=50, stretch=False, anchor="center")
        tree.column("product", width=200, stretch=False, anchor="center")
        tree.column("brand", width=100, stretch=False, anchor="center")
        tree.column("category", width=100, stretch=False, anchor="center")
        tree.column("color", width=130, stretch=False, anchor="center")
        tree.column("Selling_Price_M", width=100, stretch=False, anchor="center")
        tree.column("quantity", width=100, stretch=False, anchor="center")
        tree.heading("#0", text="No.", anchor="center")
        tree.heading("product", text="Product", anchor="center")
        tree.heading("brand", text="Brand", anchor="center")
        tree.heading("category", text="Category", anchor="center")
        tree.heading("color", text="Color", anchor="center")
        tree.heading("Selling_Price_M", text="Selling Price (M)", anchor="center")
        tree.heading("quantity", text="Quantity", anchor="center")
        tree.place(x= 110, y = 380, width = 800, height = 180)
        product_list = self.order.get_product_list()
        for i in range(len(product_list)):
            tree.insert('', 'end', text=i+1, values=(product_list[i][0], product_list[i][1], product_list[i][2], product_list[i][3], product_list[i][4], product_list[i][5]))
        
        list = None
        tree.bind("<<TreeviewSelect>>", lambda event: self.on_tree_select(event, tree, productEntry))

        # Scrollbar
        scrollBarY = ttk.Scrollbar(contentFrame, orient="vertical", command=tree.yview)
        scrollBarY.place(x=890, y=380, height=180, width = 20)
        tree.configure(yscrollcommand=scrollBarY.set)
        # Return the selected values variable instead of the tree object
        return tree
    
    def btnAdd_Order(self, fields, temp_frame, contentFrame, productEntry, tree):
        order_list = []
        has_entry = False
        for child in temp_frame.winfo_children():
            if isinstance(child, ttk.Entry):
                has_entry = True
                break
        if has_entry:
            # Bind order_list to entry.get() & delete entry
            for child in temp_frame.winfo_children():
                if isinstance(child, ttk.Entry):
                    order_list.append(child.get())
                    # child.destroy()
        
        if len(order_list) > 0:
            total_product_list = self.order.get_product_list()
            for i in range(len(total_product_list)):
                if total_product_list[i][0] == order_list[0]:
                    order_list.clear()
                    for j in range(len(total_product_list[i])):
                        order_list.append(total_product_list[i][j])
                    break
        full_order_list = []
        response = self.order.check_add_order(fields, order_list)
        if response == -1:
            messagebox.showinfo("Error", "Out of stock")
        if response > 0 and len(order_list) > 0:
            messagebox.showinfo("Success", "Add order successfully")
            for i in range(len(fields)):
                full_order_list.append(fields[i].get())
            for i in range(len(order_list)):
                full_order_list.append(order_list[i])
            time_order = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            full_order_list.insert(0, time_order)
            self.order.add(full_order_list)
        if response == 0:
            messagebox.showinfo("Error", "Add order failed")
        for i in range(len(fields)):
            fields[i].delete(0, 'end')

        # Reset order list
        tree.destroy()
        self.showTreeView_OrderProductList(contentFrame, productEntry)

    def showTreeView_OrderList(self, contentFrame, orderFrame):
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        tree = ttk.Treeview(orderFrame, height=11)
        tree["columns"] = ("Time","Customer_name", "Customer_Phone","product", "brand", "category", "color", "quantity", "Selling_Price_M")
        tree.column("#0", width=50, stretch=False, anchor="center")
        tree.column("Time", width=200, stretch=False, anchor="center")
        tree.column("Customer_name", width=200, stretch=False, anchor="center")
        tree.column("Customer_Phone", width=200, stretch=False, anchor="center")
        tree.column("product", width=200, stretch=False, anchor="center")
        tree.column("brand", width=100, stretch=False, anchor="center")
        tree.column("category", width=100, stretch=False, anchor="center")
        tree.column("color", width=130, stretch=False, anchor="center")
        tree.column("quantity", width=100, stretch=False, anchor="center")
        tree.column("Selling_Price_M", width=200, stretch=False, anchor="center")
        tree.heading("#0", text="No.", anchor="center")
        tree.heading("Time", text="Time", anchor="center")
        tree.heading("Customer_name", text="Customer Name")
        tree.heading("Customer_Phone", text="Customer Phone", anchor="center")
        tree.heading("product", text="Product", anchor="center")
        tree.heading("brand", text="Brand", anchor="center")
        tree.heading("category", text="Category", anchor="center")
        tree.heading("color", text="Color", anchor="center")
        tree.heading("quantity", text="Quantity", anchor="center")
        tree.heading("Selling_Price_M", text="Selling Price (M)", anchor="center")
        tree.place(x= 0, y = 0, width = 1000, height = 450)
        order_list = self.order.get_order_list()
        for i in range(len(order_list)):
            tree.bind("<Delete>", self.order_delete)
            tree.insert('', 'end', text=i+1, values=(order_list[i][0], order_list[i][1], order_list[i][2], order_list[i][3], order_list[i][4], order_list[i][5], order_list[i][6], order_list[i][7], order_list[i][8]))
        # Scrollbar
        scrollBarY = ttk.Scrollbar(contentFrame, orient="vertical", command=tree.yview)
        scrollBarY.place(x=990, y=160, height=440, width = 20)
        tree.configure(yscrollcommand=scrollBarY.set)
        scrollBarX = ttk.Scrollbar(contentFrame, orient="horizontal", command=tree.xview)
        scrollBarX.place(x=20, y=600, height=20, width = 970)
        tree.configure(xscrollcommand=scrollBarX.set)
        return tree

    """
        @Override
    """
    def main(self):
        self.homeView.main()