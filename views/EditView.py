import tkinter as tk
from tkinter import ttk
from views.HomeView import HoverButton as HoverButton
from views.View import View

class EditView(tk.Tk, View):
    def __init__(self,controller, root, values, frame):
        #Main
        self.window = root
        self.homeController = controller
        self.frame = frame
        self.window.geometry("880x480")
        self.window.configure(bg = "#cccccc")
        self.window.resizable(False, False)
        self.window.title("Motorcycle Store Information Management System")
        self.getEditView(values)

    def clear(self):
        self.modelInput.delete(0, tk.END)
        self.brandOption.set("")
        self.categoryOption.set("")
        self.lengthInput.delete(0, tk.END)
        self.widthInput.delete(0, tk.END)
        self.heightInput.delete(0, tk.END)
        self.massInput.delete(0, tk.END)
        self.fuelCapacityInput.delete(0, tk.END)
        self.fuelConsumptionInput.delete(0, tk.END)
        self.engineTypeInput.delete(0, tk.END)
        self.maximalEfficiencyInput.delete(0, tk.END)
        self.colorInput.delete(0, tk.END)
        self.sellingPriceInput.delete(0, tk.END)
        self.quantityInput.delete(0, tk.END)
        pass

    # def showEditView(self, values):
    #     self.clear()
    #     self.modelInput.insert(0, values[0])
    #     self.brandOption.set(values[1])
    #     self.categoryOption.set(values[2])
    #     self.lengthInput.insert(0, values[3])
    #     self.widthInput.insert(0, values[4])
    #     self.heightInput.insert(0, values[5])
    #     self.massInput.insert(0, values[6])
    #     self.fuelCapacityInput.insert(0, values[7])
    #     self.fuelConsumptionInput.insert(0, values[8])
    #     self.engineTypeInput.insert(0, values[9])
    #     self.maximalEfficiencyInput.insert(0, values[10])
    #     self.colorInput.insert(0, values[11])
    #     self.sellingPriceInput.insert(0, values[12])
    #     self.quantityInput.insert(0, values[13])
    #     global send
    #     send = []
    #     for i in range(0, len(values)):
    #         send.append(values[i])
    
    def getEditView(self, values):
        # Input for model name
        Field = []
        Field_old = []
        for i in range(0, len(values)):
            Field_old.append(values[i])
        tk.Label(self.window, text="Model:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=30, y=30)
        self.modelInput = tk.Entry(self.window, width=66, font=('Helvetica', 14))
        self.modelInput.insert(0, values[0])
        self.modelInput.place(x=120,y=30)
        Field.append(self.modelInput) 

        # Options for brand
        tk.Label(self.window, text="Brand:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=30, y=80)
        brand_name_list = []
        for i in range(len(self.homeController.brand.get_brand_list())):
            brand_name_list.append(self.homeController.brand.get_brand_list()[i][0])
        self.brandOption = ttk.Combobox(self.window, width= 24, font=('Helvetica', 14), values=brand_name_list, state='r')
        self.brandOption.set(values[1])
        self.brandOption.place(x=120, y=80)
        Field.append(self.brandOption)

        # Options for category
        tk.Label(self.window, text="Category:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=450, y=80)
        category_name_list = []
        for i in range(len(self.homeController.category.get_category_list())):
            category_name_list.append(self.homeController.category.get_category_list()[i][0])
        self.categoryOption = ttk.Combobox(self.window, width=24, font=('Helvetica', 14), values=category_name_list, state='r')
        self.categoryOption.set(values[2])
        self.categoryOption.place(x=570, y=80)
        Field.append(self.categoryOption)

        # Input for length
        tk.Label(self.window, text="Length:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=30, y=130)
        self.lengthInput = tk.Entry(self.window, width=6, font=('Helvetica', 14))
        self.lengthInput.insert(0, values[3])
        self.lengthInput.place(x=120,y=130)
        Field.append(self.lengthInput)

        # Input for width
        tk.Label(self.window, text="Width:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=250, y=130)
        self.widthInput = tk.Entry(self.window, width=6, font=('Helvetica', 14))
        self.widthInput.insert(0, values[4])
        self.widthInput.place(x=330,y=130)
        Field.append(self.widthInput)

        # Input for height
        tk.Label(self.window, text="Height:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=450, y=130)
        self.heightInput = tk.Entry(self.window, width=6, font=('Helvetica', 14))
        self.heightInput.insert(0, values[5])
        self.heightInput.place(x=535,y=130)
        Field.append(self.heightInput)

        # Input mass
        tk.Label(self.window, text="Mass:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=700, y=130)
        self.massInput = tk.Entry(self.window, width=6, font=('Helvetica', 14))
        self.massInput.insert(0, values[6])
        self.massInput.place(x=780,y=130)
        Field.append(self.massInput)

        # Input fuel capacity
        tk.Label(self.window, text="Fuel Capacity:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=30, y=180)
        self.fuelCapacityInput = tk.Entry(self.window, width=15, font=('Helvetica', 14))
        self.fuelCapacityInput.insert(0, values[7])
        self.fuelCapacityInput.place(x=230,y=180)
        Field.append(self.fuelCapacityInput)

        # Input fuel consumption
        tk.Label(self.window, text="Fuel Consumption:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=450, y=180)
        self.fuelConsumptionInput = tk.Entry(self.window, width=15, font=('Helvetica', 14))
        self.fuelConsumptionInput.insert(0, values[8])
        self.fuelConsumptionInput.place(x=680,y=180)
        Field.append(self.fuelConsumptionInput)

        # Input engine type
        tk.Label(self.window, text="Engine type:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=30, y=230)
        self.engineTypeInput = tk.Entry(self.window, width=15, font=('Helvetica', 14))
        self.engineTypeInput.insert(0, values[9])
        self.engineTypeInput.place(x=230,y=230)
        Field.append(self.engineTypeInput)

        # Input maximal efficiency
        tk.Label(self.window, text="Maximal Efficiency:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=450, y=230)
        self.maximalEfficiencyInput = tk.Entry(self.window, width=15, font=('Helvetica', 14))
        self.maximalEfficiencyInput.place(x=680,y=230)
        self.maximalEfficiencyInput.insert(0, values[10])
        Field.append(self.maximalEfficiencyInput)

        # Input color
        tk.Label(self.window, text="Color:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=30, y=280)
        self.colorInput = tk.Entry(self.window, width=15, font=('Helvetica', 14))
        self.colorInput.place(x=230,y=280)
        self.colorInput.insert(0, values[11])
        Field.append(self.colorInput)

        # Input selling price
        tk.Label(self.window, text="Selling price:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=30, y=330)
        self.sellingPriceInput = tk.Entry(self.window, width=15, font=('Helvetica', 14))
        self.sellingPriceInput.place(x=230,y=330)
        self.sellingPriceInput.insert(0, values[12])
        Field.append(self.sellingPriceInput)

        tk.Label(self.window, text="Quantity:",font=('Helvetica', 14, 'bold'), bg='#cccccc').place(x=30, y=380)
        self.quantityInput = tk.Entry(self.window, width=7, font=('Helvetica', 14))
        self.quantityInput.place(x=230,y=380)
        self.quantityInput.insert(0, values[13])
        Field.append(self.quantityInput)
        
        for i in range(len(Field)):
            if(Field[i] == ''):
                Field[i] = Field_old[i]

        updateBtn = HoverButton(self.window,text='Update',bg='#238636', fg='#fff', font=('Helvetica', 10, 'bold'), width=10, activebackground='#238636', activeforeground='#fff', relief='flat', command = lambda: self.homeController.btnUpdate_Product(Field, Field_old,self.window, self.frame)) 
        updateBtn.place(x=670, y = 420)

        clearBtn = HoverButton(self.window,text='Clear',bg='#cc0000', fg='#fff', font=('Helvetica', 10, 'bold'), width=10, activebackground='#cc0000', activeforeground='#fff', relief='flat', command = lambda: self.clear())
        clearBtn.place(x=770,y=420) 

    def main(self):
        self.mainloop()
    def close(self):
        return