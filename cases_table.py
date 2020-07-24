import pandas as pd
import tkinter as tk

class CasesTableApp(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)
        t = SimpleTable(self, 22,13)
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
        header_two = ["Infectados", "Recuperados", "Activos"] 

        # Set row 0 labels
        current_row = []
        for column in range(0,13):
            
            label = tk.Label(self, text="", 
                                borderwidth=0, width=15, font=("Courier", 10))
            label.grid(row=0, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
        self._widgets.append(current_row)
        
        # Set (0,1) label
        current_row = []
        label = tk.Label(self, text="Semana", 
                                borderwidth=0, width=15, font=("Courier", 10))
        label.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)
        current_row.append(label)
        self._widgets.append(current_row)

        # Set row 1 labels
        for column in range(1,13):
            label = tk.Label(self, text=header_two[(column % 3) - 1], 
                                borderwidth=0, width=15, font=("Courier", 10))
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

            row_data = [curico_row["Casos totales"],
                        curico_row["Recuperados totales"],
                        curico_row["Activos totales"],
                        linares_row["Casos totales"],
                        linares_row["Recuperados totales"],
                        linares_row["Activos totales"],
                        talca_row["Casos totales"],
                        talca_row["Recuperados totales"],
                        talca_row["Activos totales"],
                        total_row["Casos totales"],
                        total_row["Recuperados totales"],
                        total_row["Activos totales"]]

            label = tk.Label(self, text=row, 
                                    borderwidth=0, width=15, font=("Courier", 10))
            label.grid(row=row+2, column=0, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
            self._widgets.append(current_row)

            for index in range(len(row_data)):
                label = tk.Label(self, text=row_data[int(index)], 
                                    borderwidth=0, width=15, font=("Courier", 10))
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
        self.set(0,3,"Curicó")
        self.set(0,4,"Linares")
        self.set(0,5,"Linares")
        self.set(0,6,"Linares")
        self.set(0,7,"Talca")
        self.set(0,8,"Talca")
        self.set(0,9,"Talca")
        self.set(0,10,"Total")
        self.set(0,11,"Total")
        self.set(0,12,"Total")