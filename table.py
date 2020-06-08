import tkinter as tk

class TableApp(tk.Tk):
    def __init__(self, data, target_cases):

        tk.Tk.__init__(self)
        t = SimpleTable(self, 19,10, data, target_cases)
        t.pack(side="top", fill="x")
        t.set_header()

class SimpleTable(tk.Frame):
    def __init__(self, 
                 parent, 
                 rows, 
                 columns, 
                 data,
                 target_cases):

        self.target_cases = 'Activos' if target_cases else 'Casos'

        tk.Frame.__init__(self, parent)
        self._widgets = []

        header_two = [f"{self.target_cases} totales", f"{self.target_cases} críticos totales", f"{self.target_cases} no críticos totales"] 

        current_row = []

        for column in range(0,10):
            
            label = tk.Label(self, text="", 
                                borderwidth=0, width=22)
            label.grid(row=0, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
            self._widgets.append(current_row)
            
        current_row = []

        label = tk.Label(self, text="Semana", 
                                borderwidth=0, width=22)
        label.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)
        current_row.append(label)
        self._widgets.append(current_row)

        for column in range(1,10):
            
            label = tk.Label(self, text=header_two[(column % 3) - 1], 
                                borderwidth=0, width=22)
            label.grid(row=1, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
            self._widgets.append(current_row)

        for row in range(18):

            current_row = []

            curico_row = data[0].iloc[row]
            linares_row = data[1].iloc[row]
            talca_row = data[2].iloc[row]

            row_data = [curico_row[self.target_cases + " totales"],
                        curico_row[self.target_cases + " criticos totales"],
                        curico_row[self.target_cases + " no criticos totales"],
                        linares_row[self.target_cases + " totales"],
                        linares_row[self.target_cases + " criticos totales"],
                        linares_row[self.target_cases + " no criticos totales"],
                        talca_row[self.target_cases + " totales"],
                        talca_row[self.target_cases + " criticos totales"],
                        talca_row[self.target_cases + " no criticos totales"]]

            label = tk.Label(self, text=row, 
                                    borderwidth=0, width=22)
            label.grid(row=row+2, column=0, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
            self._widgets.append(current_row)

            for index in range(len(row_data)):
                label = tk.Label(self, text=row_data[int(index)], 
                                    borderwidth=0, width=22)
                label.grid(row=row+2, column=index+1, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
                self._widgets.append(current_row)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)
    
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