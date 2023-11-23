from tkinter import *
import tkinter.ttk as ttk
from model import ResourcesDAO

db = ResourcesDAO('RateAnalysis.db')
res_groups = ['Labor', 'Material', 'P & M', 'Sub Con', 'Others']


class ResultTreeview(ttk.Treeview):
    def __init__(self, cont, on_double_click, table_headers, **kw):
        super().__init__(cont, **kw)
        self.cont = cont
        self.on_double_click = on_double_click
        self.table_headers = table_headers
        self.cid = None
        self.rid = None
        self.set_result_headers()
        self.load_resources_data()
        self.bind('<Double-1>', self.double_clicked)

    def set_result_headers(self):
        style = ttk.Style()
        style.configure("Treeview.Treeview", padding=5)

        self.heading('#0', text='Resource\nGroup\n', anchor=CENTER)
        self.column('#0', width=100, minwidth=100, stretch=True)
        col_widths = [100, 300, 75, 100, 100, 150, 150]

        i = 0
        for col in self.table_headers:
            self.heading(col, text=col.replace('_', '\n') + '\n', anchor=CENTER)
            self.column(col, width=col_widths[i], minwidth=col_widths[i], stretch=True)
            i = i + 1

    def load_resources_data(self):
        data = db.get_all_resources()
        items = self.get_children()
        for item in items:
            self.delete(item)

        parent_row = ''
        i = 0
        for row in data:
            items = self.get_children()
            a = []
            for x in items:
                if self.item(x, 'text') not in a:
                    a.append(self.item(x, 'text'))

            rowtype = 'even-row' if i % 2 == 0 else 'odd-row'

            if row[1] not in a:
                if row[1] == 'Labor':
                    self.lab_row = self.insert(parent='', index=END, text='Labor', tags=(rowtype,))
                elif row[1] == 'Material':
                    self.mat_row = self.insert(parent='', index=END, text='Material', tags=(rowtype,))
                elif row[1] == 'P & M':
                    self.pnm_row = self.insert(parent='', index=END, text='P & M', tags=(rowtype,))
                elif row[1] == 'Sub Con':
                    self.subcon_row = self.insert(parent='', index=END, text='Sub Con', tags=(rowtype,))
                elif row[1] == 'Others':
                    self.oth_row = self.insert(parent='', index=END, text='Others', tags=(rowtype,))
                i += 1

            rowtype = 'even-row' if i % 2 == 0 else 'odd-row'

            if row[1] == 'Labor':
                parent_row = self.lab_row
            elif row[1] == 'Material':
                parent_row = self.mat_row
            elif row[1] == 'P & M':
                parent_row = self.pnm_row
            elif row[1] == 'Sub Con':
                parent_row = self.subcon_row
            elif row[1] == 'Others':
                parent_row = self.oth_row

            self.insert(parent=parent_row, index=END, values=(row[2], row[3],
                                                              row[4], row[5], row[6],
                                                              row[7], row[8]), tags=(rowtype,))
            i += 1

        self.tag_configure('even-row', background='light blue')

    def double_clicked(self, event):
        reg_clicked = self.identify_region(event.x, event.y)
        fid = self.focus()
        if reg_clicked == 'cell':
            self.cid = self.identify_column(event.x)
            self.rid = self.identify_row(event.y)
            if self.parent(fid) != '':
                selected_values = self.item(fid).get('values')
                resource_code = self.item(self.parent(fid)).get('text') + '-' + selected_values[0]
                self.on_double_click(resource_code) # Callback
