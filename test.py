import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os, time
from views.View import View
from db.settingup import SettingUp

class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.background = self['bg']
        self.bind("<Enter>", self.hover)
        self.bind("<Leave>", self.leave)
        
    def hover(self, e):
        self['bg'] = self['activebackground']
    def leave(self, e):
        self['bg'] = self.background

class HomeView(tk.Tk, View):
    def __init__(self,controller, root):
        SettingUp()
        self.window = root
        self.homeController = controller
        self.window.geometry("1280x720+100+50")
        self.window.resizable(False, False)
        self.window.title("Motorcycle Store Information Management System")
        
        userInformationFrame = tk.Frame(self.window, width=1280, height=60, bg="black")
        userInformationFrame.place(x=0, y=0)
        
        navigationFrame = tk.Frame(self.window, width=270, height=660, bg="#cc0000")
        navigationFrame.place(x=0, y=60)
        
        self.contentFrame = tk.Frame(self.window, width=1010, height=660, bg='#fff')
        self.contentFrame.place(x=270, y=60)
        
        frameCnt = 12
        file_name = '../img/login_page.gif'
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        frames = [tk.PhotoImage(file=file_path, format=f"gif -index {i}") for i in range(frameCnt)]
        for i in range(frameCnt):
            frames[i] = frames[i].subsample(3, 3)
        def update(ind):
            frame = frames[ind]
            ind += 1
            if ind == frameCnt:
                ind = 0
            try:
                self.label.configure(image=frame)
            except:
                return
            self.window.after(100, update, ind)
        self.label = tk.Label(navigationFrame, bg = "#cc0000")
        self.label.place(x = -200, y = -40)
        self.window.after(0, update, 0)     


        dashboardBtn = HoverButton(navigationFrame, width=26, fg="#fff", bg="#cc0000", text="Dashboard", font=('Helvetica', 15, 'bold'), bd=None, activebackground='#b20000', activeforeground = 'white', relief='flat', command=lambda: self.displayDashboard(self.contentFrame), cursor = 'hand2')
        dashboardBtn.place(x=-25, y=160)
        
        # Button to activate the function
        brandBtn = HoverButton(navigationFrame, width=26, fg="#fff", bg="#cc0000", text="Brand", font=('Helvetica', 15, 'bold'), bd=None, activebackground='#b20000', activeforeground = 'white', relief='flat', command=lambda: self.displayBrand(self.contentFrame), cursor = 'hand2')
        brandBtn.place(x=-27, y=205)
        
        categoryBtn = HoverButton(navigationFrame, width=26, fg="#fff", bg="#cc0000", text="Category", font=('Helvetica', 15, 'bold'), bd=None, activebackground='#b20000', activeforeground = 'white', relief='flat', command=lambda: self.displayCategory(self.contentFrame), cursor = 'hand2')
        categoryBtn.place(x=-27, y=250)
    
        addProductBtn = HoverButton(navigationFrame, width=26, fg="#fff", bg="#cc0000", text="Add Product", font=('Helvetica', 15, 'bold'), bd=None, activebackground='#b20000', activeforeground = 'white', relief='flat', command=lambda: self.displayAddProduct(self.contentFrame), cursor = 'hand2')
        addProductBtn.place(x=-25, y=295)
        
        manageProductsBtn = HoverButton(navigationFrame, width=26, fg="#fff", bg="#cc0000", text="Manage Products", font=('Helvetica', 15, 'bold'), bd=None, activebackground='#b20000', activeforeground = 'white', relief='flat', command=lambda: self.displayManageProducts(self.contentFrame), cursor = 'hand2')
        manageProductsBtn.place(x=-21, y=340)
        
        newOrderBtn = HoverButton(navigationFrame, width=26, fg="#fff", bg="#cc0000", text="New order", font=('Helvetica', 15, 'bold'), bd=None, activebackground='#b20000', activeforeground = 'white', relief='flat', command=lambda: self.displayNewOrder(self.contentFrame), cursor = 'hand2')
        newOrderBtn.place(x=-27, y=385)
        
        manageOrdersBtn = HoverButton(navigationFrame, width=26, fg="#fff", bg="#cc0000", text="Orders history", font=('Helvetica', 15, 'bold'), bd=None, activebackground='#b20000', activeforeground = 'white', relief='flat', command=lambda: self.displayManageOrders(self.contentFrame), cursor = 'hand2')
        manageOrdersBtn.place(x=-27, y=430)
        
        self.displayDashboard(self.contentFrame)
        self.move_in(navigationFrame)
    
    
    # Function to clear all widgets in frame
    def clearFrame(self, contentFrame):
        for widget in contentFrame.winfo_children():
            widget.destroy()
            
    def move_in(self, navigationFrame):
        x = -200
        while x <= 16:
            self.label.place(x=x, y=-40)
            x += 1
            time.sleep(0.01)
            navigationFrame.update()
        self.label.place(x=16, y=-40)

    # Dashboard content
    def displayDashboard(self, contentFrame):
        self.clearFrame(contentFrame)    
        tk.Label(contentFrame, text="Dashboard",font=('Helvetica', 25, 'bold'), bg='#fff').place(x=60, y=60)

        contentFrameOne = tk.Frame(contentFrame, width=440, height=202, bg='#cc0000')
        contentFrameOne.place(x=60, y=170)
        self.totalProductImg = Image.open("./img/Total_products.png")
        self.totalProductResizeImg = self.totalProductImg.resize((220, 202))
        self.totalProductResizeImg = ImageTk.PhotoImage(self.totalProductResizeImg)
        self.totalProduct = tk.Label(contentFrameOne, image=self.totalProductResizeImg, bg='#cc0000')
        self.totalProduct.place(x=0, y=0)
        tk.Label(contentFrameOne, text = self.homeController.get_sum_product(), font =("Helvetica", 40, 'bold'), bg = '#cc0000', fg='#ffffff').place(x = 270, y = 80)
        
        contentFrameTwo = tk.Frame(contentFrame, width=440, height=202, bg='#179648')
        contentFrameTwo.place(x=515, y=170)
        self.revenueImg = Image.open("./img/Revenue.png")
        self.revenueResizeImg = self.revenueImg.resize((220, 202))
        self.revenueResizeImg = ImageTk.PhotoImage(self.revenueResizeImg)
        self.revenue = tk.Label(contentFrameTwo, image=self.revenueResizeImg, bg='#179648')
        self.revenue.place(x=0, y=0)
        tk.Label(contentFrameTwo, text = self.homeController.get_profit(), font =("Helvetica", 40, 'bold'), bg = '#179648', fg='#ffffff').place(x = 180, y = 80)
        
        contentFrameThree = tk.Frame(contentFrame, width=440, height=202, bg='#263981')
        contentFrameThree.place(x=60, y=400)
        self.brandsImg = Image.open("./img/Brands.png")
        self.brandsResizeImg = self.brandsImg.resize((220, 202))
        self.brandsResizeImg = ImageTk.PhotoImage(self.brandsResizeImg)
        self.brands = tk.Label(contentFrameThree, image=self.brandsResizeImg, bg='#263981')
        self.brands.place(x=0, y=0)
        tk.Label(contentFrameThree, text = self.homeController.get_sum_brand(), font =("Helvetica", 40, 'bold'),bg='#263981', fg = '#ffffff').place(x = 290, y = 80)
        
        contentFrameFour = tk.Frame(contentFrame, width=440, height=202, bg='#f58217')
        contentFrameFour.place(x=515, y=400)
        self.soldProductsImg = Image.open("./img/Sold_products.png")
        self.soldProductsResizeImg = self.soldProductsImg.resize((220, 202))
        self.soldProductsResizeImg = ImageTk.PhotoImage(self.soldProductsResizeImg)
        self.soldProducts = tk.Label(contentFrameFour, image=self.soldProductsResizeImg, bg='#f58217')
        self.soldProducts.place(x=0, y=0)
        tk.Label(contentFrameFour, text = self.homeController.get_sum_soldproduct(), font =("Helvetica", 40, 'bold'), bg = '#f58217', fg='#ffffff').place(x = 270, y = 80)         
        
    # Brand content
    def displayBrand(self, contentFrame):
        self.clearFrame(contentFrame)
        # Label "Brand"
        tk.Label(contentFrame, text="Brand",font=('Helvetica', 25, 'bold'), bg='#fff').place(x=60, y=60)
        # Add new brand
        brandAddEntryBox = ttk.Entry(contentFrame, font = ('Helvetica', 10))
        brandAddEntryBox.place(x = 680, y = 125, width = 235, height = 25)

        saveChangeBtn = HoverButton(contentFrame, text = "Add", bg = '#238686', fg = "#fff", font = ('Helvetica', 10, 'bold'), activebackground = '#238636', activeforeground = '#fff', relief = 'flat', command = lambda: self.homeController.btnAdd_Brand(brandAddEntryBox, tree, contentFrame))
        saveChangeBtn.place(x = 915, y = 125, width = 65, height = 25)

        # Show brand list
        # Treeview
        tree = self.homeController.showTreeView_BrandList(contentFrame, self.homeController.brand.get_brand_list())   
    
    def displayCategory(self, contentFrame):
        self.clearFrame(contentFrame)   
        tk.Label(contentFrame, text="Category",font=('Helvetica', 25, 'bold'), bg='#fff').place(x=60, y=60)
        
        # Manual Motorcycle Box
        def directToManual(e):
            self.displayManageProductsByCategory(contentFrame, "manual")

        self.manualImg = Image.open("./img/manual.png")
        self.manualResizeImg = self.manualImg.resize((200, 200))
        self.manualResizeImg = ImageTk.PhotoImage(self.manualResizeImg)
        self.manual = tk.Label(contentFrame, image=self.manualResizeImg, bg='#ffffff', cursor='hand2')
        self.manual.place(x=180, y=140)
        self.manual.bind('<Button-1>', directToManual)
        
        # Scooter Box
        def directToScooter(e):
            self.displayManageProductsByCategory(contentFrame, "scooter")
        self.scooterImg = Image.open("./img/scooter.png")
        self.scooterImg = self.scooterImg.resize((200, 200))
        self.scooterImg = ImageTk.PhotoImage(self.scooterImg)
        self.scooter = tk.Label(contentFrame, image=self.scooterImg, bg='#ffffff', cursor='hand2')
        self.scooter.place(x=580, y=140)
        self.scooter.bind('<Button-1>', directToScooter)
        
        # Sport Box
        def directToSport(e):
            self.displayManageProductsByCategory(contentFrame, "sport")
        self.sportImg = Image.open("./img/sport.png")
        self.sportImg = self.sportImg.resize((200, 200))
        self.sportImg = ImageTk.PhotoImage(self.sportImg)
        self.sport = tk.Label(contentFrame, image=self.sportImg, bg='#ffffff', cursor='hand2')
        self.sport.place(x=380, y=390)
        self.sport.bind('<Button-1>', directToSport)     
        
    def displayAddProduct(self, contentFrame):
        self.clearFrame(contentFrame)
        Field = []
        tk.Label(contentFrame, text="Add product",font=('Helvetica', 25, 'bold'), bg='#fff').place(x=60, y=60)
        inputFrame = tk.Frame(contentFrame, width=890, height=470, bg='#cccccc')
        inputFrame.place(x=60, y=120)
        
        # Input for model name
        tk.Label(inputFrame, text="Model:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=30, y=30)
        modelInput = ttk.Entry(inputFrame, width=66, font=('Helvetica', 14))
        modelInput.place(x=120,y=30)
        Field.append(modelInput)
        
        # Options for brand
        tk.Label(inputFrame, text="Brand:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=30, y=80)
        brand_name_list = []
        for i in range(len(self.homeController.brand.get_brand_list())):
            brand_name_list.append(self.homeController.brand.get_brand_list()[i][0])
        brandOption = ttk.Combobox(inputFrame, width= 24, font=('Helvetica', 14), values=brand_name_list, state='r')
        brandOption.place(x=120, y=80)
        Field.append(brandOption)
        
        # Options for category
        tk.Label(inputFrame, text="Category:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=450, y=80)
        category_name_list = []
        for i in range(len(self.homeController.category.get_category_list())):
            category_name_list.append(self.homeController.category.get_category_list()[i][0])
        categoryOption = ttk.Combobox(inputFrame, width=24, font=('Helvetica', 14), values=category_name_list, state='r')
        categoryOption.place(x=570, y=80)
        Field.append(categoryOption)
        
        # Input for length
        tk.Label(inputFrame, text="Length:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=30, y=130)
        lengthInput = ttk.Entry(inputFrame, width=6, font=('Helvetica', 14))
        lengthInput.place(x=120,y=130)
        Field.append(lengthInput)
        
        # Input for width
        tk.Label(inputFrame, text="Width:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=250, y=130)
        widthInput = ttk.Entry(inputFrame, width=6, font=('Helvetica', 14))
        widthInput.place(x=330,y=130)
        Field.append(widthInput)
        
        # Input for height
        tk.Label(inputFrame, text="Height:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=450, y=130)
        heightInput = ttk.Entry(inputFrame, width=6, font=('Helvetica', 14))
        heightInput.place(x=535,y=130)
        Field.append(heightInput)
        
        # Input mass
        tk.Label(inputFrame, text="Mass:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=700, y=130)
        massInput = ttk.Entry(inputFrame, width=6, font=('Helvetica', 14))
        massInput.place(x=780,y=130)
        Field.append(massInput)
        
        # Input fuel capacity
        tk.Label(inputFrame, text="Fuel Capacity:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=30, y=180)
        fuelCapacityInput = ttk.Entry(inputFrame, width=15, font=('Helvetica', 14))
        fuelCapacityInput.place(x=230,y=180)
        Field.append(fuelCapacityInput)
        
        # Input fuel consumption
        tk.Label(inputFrame, text="Fuel Consumption:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=450, y=180)
        fuelConsumptionInput = ttk.Entry(inputFrame, width=15, font=('Helvetica', 14))
        fuelConsumptionInput.place(x=680,y=180)
        Field.append(fuelConsumptionInput)
        
        # Input engine type
        tk.Label(inputFrame, text="Engine type:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=30, y=230)
        engineTypeInput = ttk.Entry(inputFrame, width=15, font=('Helvetica', 14))
        engineTypeInput.place(x=230,y=230)
        Field.append(engineTypeInput)
        
        # Input maximal efficiency
        tk.Label(inputFrame, text="Maximal Efficiency:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=450, y=230)
        maximalEfficiencyInput = ttk.Entry(inputFrame, width=15, font=('Helvetica', 14))
        maximalEfficiencyInput.place(x=680,y=230)
        Field.append(maximalEfficiencyInput)
        
        # Input color
        tk.Label(inputFrame, text="Color:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=30, y=280)
        colorInput = ttk.Entry(inputFrame, width=15, font=('Helvetica', 14))
        colorInput.place(x=230,y=280)
        Field.append(colorInput)
        
        # Input selling price
        tk.Label(inputFrame, text="Selling price:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=30, y=330)
        sellingPriceInput = ttk.Entry(inputFrame, width=15, font=('Helvetica', 14))
        sellingPriceInput.place(x=230,y=330)
        Field.append(sellingPriceInput)
        
        tk.Label(inputFrame, text="Quantity:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=30, y=380)
        quantityInput = ttk.Entry(inputFrame, width=7, font=('Helvetica', 14))
        quantityInput.place(x=230,y=380)
        Field.append(quantityInput)

        addBtn = HoverButton(inputFrame,text='Add',bg='#238636', fg='#fff', font=('Helvetica', 10, 'bold'), width=10, activebackground='#238636', activeforeground='#fff', relief='flat', command = lambda: self.homeController.btnAdd_Product(Field))
        addBtn.place(x=670, y = 420)
        
        # Clear button
        clearBtn = HoverButton(inputFrame,text='Clear',bg='#cc0000', fg='#fff', font=('Helvetica', 10, 'bold'), width=10, activebackground='#cc0000', activeforeground='#fff', relief='flat', command = self.homeController.clearContent(Field))
        clearBtn.place(x=770,y=420)       
        
        
    def displayManageProducts(self, contentFrame):
        try:
            self.tree.destroy()
        except:
            pass
        self.clearFrame(contentFrame)   
        tk.Label(contentFrame, text="Manage products",font=('Helvetica', 25, 'bold'), bg='#fff').place(x=60, y=60)

        productFrame = tk.Frame(contentFrame, bg = "#cccccc")
        productFrame.place(x=20, y=160, width=970, height=440)

        searchBar = ttk.Entry(contentFrame, font = ('Helvetica', 10))
        searchBar.place(x=780, y=125, width=210, height=25)

        # searchBtn = HoverButton(contentFrame, text = "Search", font =('Helvetica',10, 'bold'), bg = "#238636", fg = "#ffffff", bd = 0, activebackground = "#238636", activeforeground = "#ffffff", relief = "flat",command = lambda: self.homeController.btnSearch_product(productFrame, searchBar.get()))
        # searchBtn.place(x=915, y=125, width=65, height=25)

        category_name_list = []
        for i in range(len(self.homeController.category.get_category_list())):
            category_name_list.append(self.homeController.category.get_category_list()[i][0])
        
        categoryDrop = ttk.Combobox(contentFrame, values = category_name_list, font = ('Helvetica', 10), state = "r")
        categoryDrop.set("Category")
        categoryDrop.place(x=580, y=125, width=90, height=25)
        # def filterCategory(e):
        #     self.tree = self.homeController.filterCategory(productFrame,categoryDrop.get())
        #     return self.tree
        # categoryDrop.bind("<<ComboboxSelected>>", filterCategory)        
        
        brand_name_list = []
        for i in range(len(self.homeController.brand.get_brand_list())):
            brand_name_list.append(self.homeController.brand.get_brand_list()[i][0])
        brandDrop = ttk.Combobox(contentFrame, values=brand_name_list, font = ('Helvetica', 10), state = "r")
        brandDrop.set("Filter")
        brandDrop.place(x=680, y=125, width=90, height=25)

        # def filterBrand(e):
        #     self.tree = self.homeController.filterBrand(productFrame,brandDrop.get())
        #     return self.tree
        # brandDrop.bind("<<ComboboxSelected>>", filterBrand)
        
        # def filterDropCallback(event):
        #     if filterDrop.get() == 'Brand':
        #         new_tree = self.homeController.filterDropCallback(productFrame,'brand')
        #     elif filterDrop.get() == 'Category':
        #         new_tree = self.homeController.filterDropCallback(productFrame,'category')
        #     return new_tree
        # filterDrop.bind("<<ComboboxSelected>>", filterDropCallback)

        sortDrop = ttk.Combobox(contentFrame,values=['Name', 'Selling_Price_M'] , font = ('Helvetica', 10), state = "r")
        sortDrop.set("Sort")
        sortDrop.place(x=480, y=125, width=90, height=25)
        # def sortDropCallback(event):
        #     if sortDrop.get() == 'Name':
        #         print("5")
        #         new_tree = self.homeController.sortDropCallback(productFrame,'Name')
        #     elif sortDrop.get() == 'Price':
        #         new_tree = self.homeController.sortDropCallback(productFrame,'Selling_Price_M')
        #         return new_tree
        # sortDrop.bind("<<ComboboxSelected>>", sortDropCallback)

        # Treeview
        self.tree = self.homeController.showTreeView_ProductList(productFrame, searchBar.get(), sortDrop.get(), categoryDrop.get(), brandDrop.get())
        def searchByContent(e):
            self.tree = self.homeController.showTreeView_ProductList(productFrame, searchBar.get(), sortDrop.get(), categoryDrop.get(), brandDrop.get())
            return self.tree
        searchBar.bind('<KeyRelease>', searchByContent)
        
        sortDrop.bind("<<ComboboxSelected>>", searchByContent)
        brandDrop.bind("<<ComboboxSelected>>", searchByContent)
        categoryDrop.bind("<<ComboboxSelected>>", searchByContent)

    def displayManageProductsByCategory(self, contentFrame, category):
        try:
            self.tree.destroy()
        except:
            pass
        self.clearFrame(contentFrame)   
        tk.Label(contentFrame, text="Manage products",font=('Helvetica', 25, 'bold'), bg='#fff').place(x=60, y=60)

        productFrame = tk.Frame(contentFrame, bg = "#cccccc")
        productFrame.place(x=20, y=160, width=970, height=440)

        searchBar = ttk.Entry(contentFrame, font = ('Helvetica', 10))
        searchBar.place(x=780, y=125, width=210, height=25)

        # searchBtn = HoverButton(contentFrame, text = "Search", font = ('Helvetica',10, 'bold'), bg = "#238636", fg = "#ffffff", bd = 0, activebackground = "#238636", activeforeground = "#ffffff", relief = "flat",command = lambda: self.homeController.btnSearch_product(productFrame, searchBar.get()))
        # searchBtn.place(x=915, y=125, width=65, height=25)

        category_name_list = []
        for i in range(len(self.homeController.category.get_category_list())):
            category_name_list.append(self.homeController.category.get_category_list()[i][0])
        
        categoryDrop = ttk.Combobox(contentFrame, values = category_name_list, font = ('Helvetica', 10), state = "r")
        categoryDrop.set(category)
        categoryDrop.place(x=580, y=125, width=90, height=25)
        # def filterCategory(e):
        #     self.tree = self.homeController.filterCategory(productFrame,categoryDrop.get())
        #     return self.tree
        # categoryDrop.bind("<<ComboboxSelected>>", filterCategory)        
        
        brand_name_list = []
        for i in range(len(self.homeController.brand.get_brand_list())):
            brand_name_list.append(self.homeController.brand.get_brand_list()[i][0])
        brandDrop = ttk.Combobox(contentFrame, values=brand_name_list, font = ('Helvetica', 10), state = "r")
        brandDrop.set("Filter")
        brandDrop.place(x=680, y=125, width=90, height=25)
        # def filterBrand(e):
        #     self.tree = self.homeController.filterBrand(productFrame,brandDrop.get())
        #     return self.tree
        # brandDrop.bind("<<ComboboxSelected>>", filterBrand)
        
        # def filterDropCallback(event):
        #     if filterDrop.get() == 'Brand':
        #         new_tree = self.homeController.filterDropCallback(productFrame,'brand')
        #     elif filterDrop.get() == 'Category':
        #         new_tree = self.homeController.filterDropCallback(productFrame,'category')
        #     return new_tree
        # filterDrop.bind("<<ComboboxSelected>>", filterDropCallback)

        sortDrop = ttk.Combobox(contentFrame,values=['Name', 'Selling_Price_M'] , font = ('Helvetica', 10), state = "r")
        sortDrop.set("Sort")
        sortDrop.place(x=480, y=125, width=90, height=25)
        # def sortDropCallback(event):
        #     if sortDrop.get() == 'Name':
        #         print("5")
        #         new_tree = self.homeController.sortDropCallback(productFrame,'Name')
        #     elif sortDrop.get() == 'Price':
        #         new_tree = self.homeController.sortDropCallback(productFrame,'Selling_Price_M')
        #         return new_tree
        # sortDrop.bind("<<ComboboxSelected>>", sortDropCallback)

        # Treeview
        self.tree = self.homeController.showTreeView_ProductList(productFrame, searchBar.get(), sortDrop.get(), categoryDrop.get(), brandDrop.get())
        def searchByContent(e):
            self.tree = self.homeController.showTreeView_ProductList(productFrame, searchBar.get(), sortDrop.get(), categoryDrop.get(), brandDrop.get())
            return self.tree
        searchBar.bind('<KeyRelease>', searchByContent)
        
        sortDrop.bind("<<ComboboxSelected>>", searchByContent)
        brandDrop.bind("<<ComboboxSelected>>", searchByContent)
        categoryDrop.bind("<<ComboboxSelected>>", searchByContent)
        
    def displayNewOrder(self, contentFrame):   
        self.clearFrame(contentFrame)
        Field = []
        tk.Label(contentFrame, text="New order",font=('Helvetica', 25, 'bold'), bg='#fff').place(x=60, y=60)
        
        customerInformationFrame = tk.Frame(contentFrame, height=180, width=890, bg='#cccccc')
        customerInformationFrame.place(x=60, y=120)
        tk.Label(customerInformationFrame, text="Customer Information:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=10, y=10)
        
        tk.Label(customerInformationFrame, text="Name:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=40, y=60)
        customerNameInput = ttk.Entry(customerInformationFrame, width=22, font=('Helvetica', 14))
        customerNameInput.place(x=150,y=60)
        Field.append(customerNameInput)

        tk.Label(customerInformationFrame, text="Phone:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=40, y=120)
        phoneInput = ttk.Entry(customerInformationFrame, width=22, font=('Helvetica', 14))
        phoneInput.place(x=150,y=120)
        Field.append(phoneInput)

        modelInformationFrame = tk.Frame(contentFrame, height=290, width=890, bg='#cccccc')
        modelInformationFrame.place(x=60, y=330)
        tk.Label(modelInformationFrame, text="Product bought:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=10, y=10)

        tempFrame = tk.Frame(contentFrame, height=80, width=400, bg='#cccccc')
        tempFrame.place(x=500, y=200)
        tk.Label(tempFrame, text="Product:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=0,y=0)

        def clearContent():
            customerNameInput.delete(0, tk.END)
            phoneInput.delete(0, tk.END)

        def getContent():
            pass
        
        self.tree = self.homeController.showTreeView_OrderProductList(contentFrame, tempFrame)

        clearBtn = HoverButton(modelInformationFrame,text='Clear',bg='#cc0000', fg='#fff', font=('Helvetica', 10, 'bold'), width=10, activebackground='#cc0000', activeforeground='#fff', relief='flat', command=clearContent)
        clearBtn.place(x=690, y=250)

        addBtn = HoverButton(modelInformationFrame,text='Add',bg='#238636', fg='#fff', font=('Helvetica', 10, 'bold'), width=10, activebackground='#238636', activeforeground='#fff', relief='flat', command=lambda: self.homeController.btnAdd_Order(Field, tempFrame))
        addBtn.place(x=790,y=250)
        
    def displayManageOrders(self, contentFrame):
        self.clearFrame(contentFrame)
        tk.Label(contentFrame, text="Orders history",font=('Helvetica', 25, 'bold'), bg='#fff').place(x=60, y=60)  

        orderFrame = tk.Frame(contentFrame, bg = "#cccccc")
        orderFrame.place(x=20, y=160, width=970, height=440) 

        # Treeview
        self.tree = self.homeController.showTreeView_OrderList(orderFrame)
        
    def main(self):
        self.mainloop()
    def close(self):
        return        
# def main():
#     root = tk.Tk()
#     program = Main(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()