import pandas as pd
import tkinter as tk

class CostsTableApp(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)
        t = SimpleTable(self, 21,5)
        t.pack(side="top", fill="x")
        t.set_header()

class SimpleTable(tk.Frame):
    def __init__(self, 
                 parent, 
                 rows, 
                 columns):

        tk.Frame.__init__(self, parent)
        self._widgets = []

        # Load data
        curico_data = pd.read_csv('solved_purchase_costs_Curicó.csv', encoding='iso-8859-1')
        linares_data = pd.read_csv('solved_purchase_costs_Linares.csv', encoding='iso-8859-1')
        talca_data = pd.read_csv('solved_purchase_costs_Talca.csv', encoding='iso-8859-1')
        total_data = pd.read_csv('solved_purchase_costs_total.csv', encoding='iso-8859-1')

        # Set headers
        header = "Ventiladores a enviar"

        # Set row 0 labels
        current_row = []
        for column in range(0,5):
            
            label = tk.Label(self, text="", 
                                borderwidth=0, width=30, font=("Courier", 8))
            label.grid(row=0, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
        self._widgets.append(current_row)
        
        # Set (0,1) label
        current_row = []
        label = tk.Label(self, text="Semana", 
                                borderwidth=0, width=30, font=("Courier", 8))
        label.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)
        current_row.append(label)
        self._widgets.append(current_row)

        # Set row 1 labels
        for column in range(1,5):
 
            label = tk.Label(self, text=header, 
                                borderwidth=0, width=30, font=("Courier", 8))
            label.grid(row=1, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
        self._widgets.append(current_row)

        # Set table values from data
        for row in range(18):
            current_row = []

            curico_row = curico_data.iloc[row]
            linares_row = linares_data.iloc[row]
            talca_row = talca_data.iloc[row]
            total_row = total_data.iloc[row]

            label = tk.Label(self, text=row, 
                                    borderwidth=0, width=30, font=("Courier", 8))
            label.grid(row=row+2, column=0, sticky="nsew", padx=1, pady=1)
            current_row.append(label)

            for index in range(4):
                text = "Var x"

                row_data = [curico_row[text],
                            linares_row[text],
                            talca_row[text],
                            total_row[text]]

                label = tk.Label(self, text=row_data[int(index)], 
                                    borderwidth=0, width=30, font=("Courier", 8))
                label.grid(row=row+2, column=index+1, sticky="nsew", padx=1, pady=1)
                current_row.append(label)

            self._widgets.append(current_row)
        
        # Set row 20 labels
        current_row = []
        for column in range(0,5):

            label = tk.Label(self, text="", 
                                borderwidth=0, width=30, font=("Courier", 10))
            label.grid(row=20, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
        self._widgets.append(current_row)

        # Get costs
        curico_data_inventory = pd.read_csv('solved_inventory_costs_Curicó.csv', encoding='iso-8859-1')
        linares_data_inventory = pd.read_csv('solved_inventory_costs_Linares.csv', encoding='iso-8859-1')
        talca_data_inventory = pd.read_csv('solved_inventory_costs_Talca.csv', encoding='iso-8859-1')
        total_data_inventory = pd.read_csv('solved_inventory_costs_total.csv', encoding='iso-8859-1')

        curico_purchase_costs = curico_data["Costos compra"].sum()
        linares_purchase_costs = linares_data["Costos compra"].sum()
        talca_purchase_costs = talca_data["Costos compra"].sum()
        total_purchase_costs = total_data["Costos compra"].sum()
        purchase_costs = [curico_purchase_costs,
                          linares_purchase_costs,
                          talca_purchase_costs,
                          total_purchase_costs]

        curico_inventory_costs = curico_data_inventory["Costos inventario"].sum()
        linares_inventory_costs = linares_data_inventory["Costos inventario"].sum()
        talca_inventory_costs = talca_data_inventory["Costos inventario"].sum()
        total_inventory_costs = total_data_inventory["Costos inventario"].sum()
        inventory_costs = [curico_inventory_costs,
                          linares_inventory_costs,
                          talca_inventory_costs,
                          total_inventory_costs]

        # Set row 21 labels
        current_row = []

        purchaseLabel = tk.Label(self, text="Costos compra", 
                                    borderwidth=0, width=15, font=("Courier", 10))
        purchaseLabel.grid(row=21, column=0, sticky="nsew", padx=1, pady=1)

        for column in range(1,5):
            label = tk.Label(self, text=str(purchase_costs[column - 1]), 
                                borderwidth=0, width=30, font=("Courier", 10))
            label.grid(row=21, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)

        current_row.append(purchaseLabel)
        self._widgets.append(current_row)

        # Set row 22 labels
        current_row = []

        inventoryLabel = tk.Label(self, text="Costos de inventario", 
                                    borderwidth=0, width=15, font=("Courier", 10))
        inventoryLabel.grid(row=22, column=0, sticky="nsew", padx=1, pady=1)

        for column in range(1,5):
            label = tk.Label(self, text=str(inventory_costs[column - 1]), 
                                borderwidth=0, width=30, font=("Courier", 10))
            label.grid(row=22, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)

        current_row.append(inventoryLabel)
        self._widgets.append(current_row)

        # Set row 23 labels
        current_row = []

        inventoryLabel = tk.Label(self, text="Costos totales", 
                                    borderwidth=0, width=15, font=("Courier", 10))
        inventoryLabel.grid(row=23, column=0, sticky="nsew", padx=1, pady=1)

        for column in range(1,5):
            label = tk.Label(self, text=str(purchase_costs[column - 1] + inventory_costs[column - 1]), 
                                borderwidth=0, width=30, font=("Courier", 10))
            label.grid(row=23, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)

        current_row.append(inventoryLabel)
        self._widgets.append(current_row) 

    # Set text of a cell
    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)
    
    # Set headers
    def set_header(self):
        self.set(0,0,"")
        self.set(0,1,"Curicó")
        self.set(0,2,"Linares")
        self.set(0,3,"Talca")
        self.set(0,4,"Total")