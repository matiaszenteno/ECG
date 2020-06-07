import tkinter as tk

class ExampleApp(tk.Tk):
    def __init__(self, curico_weeks_data, linares_weeks_data, talca_weeks_data):
        tk.Tk.__init__(self)
        t = SimpleTable(self, 19,10, curico_weeks_data, linares_weeks_data, talca_weeks_data)
        t.pack(side="top", fill="x")
        t.set_header()

class SimpleTable(tk.Frame):
    def __init__(self, parent, rows, columns, curico_weeks_data, linares_weeks_data, talca_weeks_data):
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent)
        self._widgets = []

        header_two = ["Activos totales", "Activos críticos totales", "Activos no críticos totales"] 

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

            print(curico_weeks_data)
            print(row)

            curico_row = curico_weeks_data.iloc[row]
            linares_row = linares_weeks_data.iloc[row]
            talca_row = talca_weeks_data.iloc[row]

            row_data = [curico_row["Activos totales"],
                        curico_row["Activos críticos totales"],
                        curico_row["Activos no críticos totales"],
                        linares_row["Activos totales"],
                        linares_row["Activos críticos totales"],
                        linares_row["Activos no críticos totales"],
                        talca_row["Activos totales"],
                        talca_row["Activos críticos totales"],
                        talca_row["Activos no críticos totales"]]

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