import pandas as pd
import tkinter as tk

class CostsTableApp(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)
        t = SimpleTable(self, 19,5)
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
        curico_data = pd.read_csv('simulation_Curicó_per_week.csv', encoding='iso-8859-1')
        linares_data = pd.read_csv('simulation_Linares_per_week.csv', encoding='iso-8859-1')
        talca_data = pd.read_csv('simulation_Talca_per_week.csv', encoding='iso-8859-1')
        total_data = pd.read_csv('simulation_total_per_week.csv', encoding='iso-8859-1')

        # Set headers
        header = "Ventiladores a enviar"

        # Set row 0 labels
        current_row = []
        for column in range(0,5):
            
            label = tk.Label(self, text="", 
                                borderwidth=0, width=30, font=("Courier", 10))
            label.grid(row=0, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
        self._widgets.append(current_row)
        
        # Set (0,1) label
        current_row = []
        label = tk.Label(self, text="Semana", 
                                borderwidth=0, width=30, font=("Courier", 10))
        label.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)
        current_row.append(label)
        self._widgets.append(current_row)

        # Set row 1 labels
        for column in range(1,5):
            label = tk.Label(self, text=header, 
                                borderwidth=0, width=30, font=("Courier", 10))
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

            row_data = [curico_row["Ventiladores requeridos"],
                        linares_row["Ventiladores requeridos"],
                        talca_row["Ventiladores requeridos"],
                        total_row["Ventiladores requeridos"]]

            label = tk.Label(self, text=row, 
                                    borderwidth=0, width=30, font=("Courier", 10))
            label.grid(row=row+2, column=0, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
            self._widgets.append(current_row)

            for index in range(len(row_data)):
                label = tk.Label(self, text=row_data[int(index)], 
                                    borderwidth=0, width=30, font=("Courier", 10))
                label.grid(row=row+2, column=index+1, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
                self._widgets.append(current_row)

        self.show_costs()

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

    # Show costs
    def show_costs(self):

        # Set row 18 labels
        current_row = []
        for column in range(0,5):
            
            label = tk.Label(self, text="", 
                                borderwidth=0, width=30, font=("Courier", 10))
            label.grid(row=18, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
        self._widgets.append(current_row)
        
        # Set row 19 labels
        current_row = []

        purchaseLabel = tk.Label(self, text="Costo compra", 
                                    borderwidth=0, width=15, font=("Courier", 10))
        purchaseLabel.grid(row=19, column=0, sticky="nsew", padx=1, pady=1)
        purchaseValueLabel = tk.Label(self, text="$$$", 
                                    borderwidth=0, width=15, font=("Courier", 10))
        purchaseValueLabel.grid(row=19, column=1, sticky="nsew", padx=1, pady=1)

        for column in range(2,5):
            
            label = tk.Label(self, text="", 
                                borderwidth=0, width=30, font=("Courier", 10))
            label.grid(row=19, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)

        current_row.append(purchaseLabel)
        current_row.append(purchaseValueLabel)

        self._widgets.append(current_row)

        # Set row 20 labels
        current_row = []

        inventoryLabel = tk.Label(self, text="Costo inventario", 
                                    borderwidth=0, width=15, font=("Courier", 10))
        inventoryLabel.grid(row=20, column=0, sticky="nsew", padx=1, pady=1)
        inventoryValueLabel = tk.Label(self, text="$$$", 
                                    borderwidth=0, width=15, font=("Courier", 10))
        inventoryValueLabel.grid(row=20, column=1, sticky="nsew", padx=1, pady=1)

        for column in range(2,5):
            
            label = tk.Label(self, text="", 
                                borderwidth=0, width=30, font=("Courier", 10))
            label.grid(row=20, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)

        current_row.append(inventoryLabel)
        current_row.append(inventoryValueLabel)

        self._widgets.append(current_row)