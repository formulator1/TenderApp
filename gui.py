import sqlite3
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox

from model import ResourcesDAO
from tree_view import ResultTreeview

db = ResourcesDAO('RateAnalysis.db')
res_groups = ['Labor', 'Material', 'P & M', 'Sub Con', 'Others']

class TenderApp:
    results_frame = None
    input_frame = None
    resource_type_dropdown = None
    text_boxes = {}  # dict to store all textbox references
    buttons = {}  # dict to store all button references
    table_headers = None
    def __init__(self, root):
        if not hasattr(self, 'root'):
            self.root = root
            self.get_resource_table_headers()
            self.build_gui()

    def get_resource_table_headers(self):
        table_headers = db.get_table_headers('RESOURCES')
        table_headers.remove('RESOURCE_GROUP')
        table_headers.remove('RESOURCE_CODE')
        TenderApp.table_headers = table_headers

    def build_gui(self):
        self.create_menu()
        Label(self.root, text='ABC Company').place(x=0, y=0, relwidth=1)

    def create_frames(self):
        if TenderApp.input_frame:
            self.create_results_frame()
        else:
            main_frame = Frame(self.root, relief='raised', borderwidth=5)
            main_frame.place(x=0, y=20, relwidth=1, relheight=1)
            TenderApp.results_frame = self.create_results_frame()
            TenderApp.input_frame = self.create_input_frame()

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        # File menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Project")
        file_menu.add_command(label="New Project")
        file_menu.add_separator()
        file_menu.add_command(label="Save Project")
        file_menu.add_command(label="Save Project As")
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.quit_application)
        # Resources menu
        resources_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Resources", menu=resources_menu)
        resources_menu.add_command(label="Show Resources", command=self.create_frames)
        resources_menu.add_command(label="Import from CSV file")
        resources_menu.add_command(label="Export to CSV file")

    def create_results_frame(self):
        frame = Frame(self.root, relief='raised', borderwidth=5)
        frame.place(x=0, y=0, relwidth=0.65, relheight=.95)
        result_tree = ResultTreeview(frame, columns=self.table_headers, height=27,
                                     on_double_click=self.on_treeview_double_click,
                                     table_headers = self.table_headers)

        verScroll = ttk.Scrollbar(frame, orient='vertical', command=result_tree.yview)
        verScroll.pack(side='right', fill='y')
        horScroll = ttk.Scrollbar(frame, orient='horizontal', command=result_tree.xview)
        horScroll.pack(side='top', fill='x')
        result_tree.pack()
        return frame

    def on_treeview_double_click(self, resource_code):
        # Resource data can be passed from Treeview widget to avoid below DB read operation
        record = db.get_resource_by_code(resource_code)
        self.populate_input_frame_with_resource_data(record)
        TenderApp.buttons['MODIFY'].configure(state='normal')
        TenderApp.buttons['DELETE'].configure(state='normal')

    def populate_input_frame_with_resource_data(self, record):
        set_text(TenderApp.resource_type_dropdown, record[1])
        set_text(TenderApp.text_boxes['SHORT_CODE'], record[2])
        set_text(TenderApp.text_boxes['RESOURCE_NAME'], record[3])
        set_text(TenderApp.text_boxes['UNIT'], record[4])
        set_text(TenderApp.text_boxes['STD_RATE'], record[5])
        set_text(TenderApp.text_boxes['PROJECT_RATE'], record[6])
        set_text(TenderApp.text_boxes['CONSUMPTION'], record[7])
        set_text(TenderApp.text_boxes['PRODUCTION'], record[8])

    def create_input_frame(self):
        frame = Frame(self.root, relief='raised', borderwidth=5)
        frame.place(relx=0.65, y=0, relwidth=0.35, relheight=.95)

        Label(frame, text='Manage Resource', font=('Arial', 15)).grid(row=0, column=0, pady=15, columnspan=3)
        Label(frame, text='Resource Group').grid(row=1, column=0, pady=15)
        Label(frame, text=' : ', justify='center').grid(row=1, column=1)
        TenderApp.resource_type_dropdown = ttk.Combobox(frame, values=res_groups)
        self.resource_type_dropdown.grid(row=1, column=2, sticky='w')

        i = 2
        for col in self.table_headers:
            # Create labels
            (Label(frame, text=col.replace('_', ' ').title(), anchor='e', justify='right')
             .grid(row=i, column=0, padx=(20, 0), pady=10, sticky='e'))
            Label(frame, text=' : ', justify='center').grid(row=i, column=1)

            # Create TextBoxes
            TenderApp.text_boxes[col] = Entry(frame, width=40)
            TenderApp.text_boxes[col].grid(row=i, column=2)
            i += 1

        # Create buttons
        btn_clear = Button(frame, text='Clear', width=15, underline=0,
                           command=self.clear_form)
        btn_save = Button(frame, text='Save', width=15, underline=0, command=self.save_record)
        btn_modify = Button(frame, text='Modify', width=15, underline=0, state='disabled', command=self.modify_record)
        btn_delete = Button(frame, text='Delete', width=15, underline=0, command=self.delete_record,
                            state='disabled')
        btn_clear.grid(row=i + 7, column=0, pady=(15, 0))
        btn_save.grid(row=i + 7, column=2, pady=(15, 0))
        btn_modify.grid(row=i + 8, column=0)
        btn_delete.grid(row=i + 8, column=2)

        TenderApp.buttons['SAVE'] = btn_save
        TenderApp.buttons['MODIFY'] = btn_modify
        TenderApp.buttons['CLEAR'] = btn_clear
        TenderApp.buttons['DELETE'] = btn_delete
        return frame

    def clear_form(self):
        for item in self.input_frame.winfo_children():
            if isinstance(item, Entry):
                item.delete(0, END)

    def save_record(self):
        resource_data = [textbox.get() for textbox in self.text_boxes.values()]

        resource_type = self.resource_type_dropdown.get()
        resource_code = self.text_boxes['SHORT_CODE'].get()

        if resource_type != '' and resource_code != '':
            resource_data.insert(0, resource_type)
            resource_data.insert(0, resource_type + '-' + resource_code)
        print(resource_data)

        try:
            db.insert_resource(resource_data)
            self.clear_form()
            messagebox.showinfo("Success", "Record inserted successfully")
            self.create_frames()
        except sqlite3.IntegrityError:
            messagebox.showinfo("Failed", "Record already exists")
        except Exception as e:
            messagebox.showinfo("Error", "Please verify data")
            print(f'\n*** ERROR ***: [save_record] - {e} \n')

    def modify_record(self):
        resource_data = [textbox.get() for textbox in self.text_boxes.values()]
        resource_type = self.resource_type_dropdown.get()
        short_code = self.text_boxes['SHORT_CODE'].get()  # resource_data[0]
        resource_code = f'{resource_type}-{short_code}'

        resource_data = resource_data[1:]
        if resource_type != '' and short_code != '':
            try:
                db.update_resource(resource_code, resource_data)
                self.clear_form()
                messagebox.showinfo("Success", "Record updated successfully")
                self.create_frames()
            except sqlite3.IntegrityError:
                messagebox.showinfo("Failed", "Record already exists")
            except Exception as e:
                messagebox.showinfo("Error", "Please verify data")
                print(f'\n*** ERROR ***: [modify_record] - {e} \n')
        else:
            messagebox.showinfo("", "Please enter Resource group & Short code")

    def delete_record(self):
        resource_type = self.resource_type_dropdown.get()
        short_code = self.text_boxes['SHORT_CODE'].get()

        if resource_type != '' and short_code != '':
            resource_code = f'{resource_type}-{short_code}'
            try:
                db.delete_resource(resource_code)
                self.clear_form()
                messagebox.showinfo("Success", "Record deleted successfully")
                self.create_frames()
            except Exception as e:
                messagebox.showinfo("Error", "Unable to delete record")
                print(f'\n*** ERROR ***: [modify_record] - {e} \n')
        else:
            messagebox.showinfo("", "Please enter Resource group & Short code")

    def quit_application(self):
        # Display a confirmation dialog
        confirmation = messagebox.askokcancel("Confirmation", "Are you sure you want to quit?")
        if confirmation:
            self.root.destroy()


def set_text(widget, text):
    widget.delete(0, END)
    widget.insert(0, text)
