import pandas as pd
import tkinter as tk

class CostsTableApp(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)
        t = SimpleTable(self, 19,9)
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
        curico_data = pd.read_csv('solved_Curicó.csv', encoding='iso-8859-1')
        linares_data = pd.read_csv('solved_Linares.csv', encoding='iso-8859-1')
        talca_data = pd.read_csv('solved_Talca.csv', encoding='iso-8859-1')
        total_data = pd.read_csv('solved_total.csv', encoding='iso-8859-1')

        # Set headers
        header_two = ["Ventiladores a enviar","Inventario"]

        # Set row 0 labels
        current_row = []
        for column in range(0,9):
            
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
        for column in range(1,9):
 
            label = tk.Label(self, text=header_two[1-column%2], 
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

            for index in range(8):

                if (1- index % 2):
                    text = "Var x"
                else:
                    text = "Var y"

                row_data = [curico_row[text],
                            linares_row[text],
                            talca_row[text],
                            total_row[text]]


                label = tk.Label(self, text=row_data[int(index)//2], 
                                    borderwidth=0, width=30, font=("Courier", 8))
                label.grid(row=row+2, column=index+1, sticky="nsew", padx=1, pady=1)
                current_row.append(label)

            self._widgets.append(current_row)

        # Set row 18 labels
        current_row = []
        for column in range(0,9):
            
            label = tk.Label(self, text="", 
                                borderwidth=0, width=30, font=("Courier", 8))
            label.grid(row=18, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
        self._widgets.append(current_row)
        
        # Set  (19,0) label
        current_row = []

        purchaseLabel = tk.Label(self, text="Costos asociados", 
                                    borderwidth=0, width=15, font=("Courier", 8))
        purchaseLabel.grid(row=19, column=0, sticky="nsew", padx=1, pady=1)
        current_row.append(purchaseLabel)

        curico_total = curico_data.sum()
        linares_total = linares_data.sum()
        talca_total = talca_data.sum()
        total_total = total_data.sum()

        for index in range(8):

            if (1- index % 2):
                text = "Costos compra"
            else:
                text = "Costos inventario"

            row_data = [curico_total[text],
                        linares_total[text],
                        talca_total[text],
                        total_total[text]]

            label = tk.Label(self, text=row_data[int(index)//2], 
                                borderwidth=0, width=30, font=("Courier", 8))
            label.grid(row=row+2, column=index+1, sticky="nsew", padx=1, pady=1)

            current_row.append(label)

        self._widgets.append(current_row)

    # Set text of a cell
    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)
    
    # Set headers
    def set_header(self):
        self.set(0,0,"")
        self.set(0,1,"Curicó")
        self.set(0,2,"Curicó")
        self.set(0,3,"Linares")
        self.set(0,4,"Linares")
        self.set(0,5,"Talca")
        self.set(0,6,"Talca")
        self.set(0,7,"Total")
        self.set(0,8,"Total")