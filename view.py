import controller
from db_manager import DBManager
import tkinter.messagebox as tmb
from tkinter import Tk, Text, Entry, Button, Label, Scrollbar, StringVar, ttk, Frame
import string


class View(Tk):
    def __init__(self, controller):
        Tk.__init__(self)
        self.definition = Text(self, wrap='word', state='disabled')
        self.additional_info = Text(self, wrap='word')
        self.textvariable = StringVar()
        self.controller = controller
        self.table = ttk.Treeview(self, columns=2)
        self.db_manager = DBManager()
        self.current_records = []
        self.create_gui()
        self.resizable(False, False)

    def create_gui(self):
        Label(self, text='Find word definition:').grid(row=0, sticky='w')
        Entry(self, textvariable=self.textvariable).grid(row=1, column=0, sticky='nsew')
        self.grid_columnconfigure(0, weight=1)
        Button(self, text='Find', command=self.on_button_find_clicked).grid(row=1, column=1, columnspan=2, sticky='nsew')
        Label(self, text='Definition:').grid(row=2, column=0, sticky='w')
        self.create_text_widget(self.definition, row=3, column=0, columnspan=2)
        Label(self, text='Additional information:').grid(row=4, column=0, sticky='w')
        self.create_text_widget(self.additional_info, row=5, column=0, columnspan=2)
        Button(self, text='Save', command=self.on_button_save_clicked).grid(row=6, column=1, sticky='nsew')
        self.create_table_view()
        self.create_table_switch_buttons()

    def create_text_widget(self, text_widget, row=0, column=0, columnspan=0):
        text_widget.grid(row=row, column=column, columnspan=columnspan)
        scrollbar = Scrollbar(self, command=text_widget.yview)
        scrollbar_column = columnspan
        scrollbar.grid(row=row, column=scrollbar_column, sticky='nsew')
        text_widget['yscrollcommand'] = scrollbar.set

    def create_table_view(self):
        self.table.grid(row=0, column=3, rowspan=6, sticky='nsew')
        scrollbar = Scrollbar(self, command=self.table.yview)
        scrollbar.grid(row=0, column=4, rowspan=6, sticky='nsew')
        self.table['yscrollcommand'] = scrollbar.set
        self.table.heading(column='#0', text='Word', anchor='w')
        self.table.heading(column=2, text='Score', anchor='w')
        self.table.bind('<ButtonRelease-1>', self.view_selected_item)
        self.table.bind('<KeyRelease-Up>', self.view_selected_item)
        self.table.bind('<KeyRelease-Down>', self.view_selected_item)

    def create_table_switch_buttons(self):
        frame = Frame(self)
        frame.grid(row=6, column=3, sticky='nsew')
        letter_iterator = iter(list(string.ascii_uppercase))
        row_count = 2
        column_count = 13
        for row in range(0, row_count):
            for column in range(0, column_count):
                letter = next(letter_iterator)
                Button(frame, text=letter, command=lambda table_name=letter: self.view_table(table_name)).grid(row=row, column=column, sticky='nsew')

    def view_table(self, table_name):
        self.clear_all()
        records = self.db_manager.get_records(table_name)
        for row in records:
            self.current_records.append(row)
            self.table.insert('', 0, text=row[0], values=row[3])

    def clear_all(self):
        items = self.table.get_children()
        for item in items:
            self.table.delete(item)
        self.textvariable.set('')
        self.clear_definition()
        self.additional_info.delete('1.0', 'end')

    def on_button_find_clicked(self):
        self.clear_definition()
        word = self.textvariable.get()
        if not word:
            tmb.showwarning('Warning', 'Word entry is empty')
            self.definition.config(state='disabled')
            return
        status, result = self.controller.get_word_definition(word)
        if status:
            for word_type in result:
                self.insert_to_definition(word_type + '\n')
                for num, text in enumerate(result[word_type], 1):
                    self.insert_to_definition(f'{num}) {text}\n')
        else:
            tmb.showerror('Error', result)

    def clear_definition(self):
        self.definition.config(state='normal')
        self.definition.delete('1.0', 'end')
        self.definition.config(state='disabled')

    def insert_to_definition(self, text):
        self.definition.config(state='normal')
        self.definition.delete('1.0', 'end')
        self.definition.insert('insert', text)
        self.definition.config(state='disabled')

    def on_button_save_clicked(self):
        table_name = self.textvariable.get()[0]
        parameters = (self.textvariable.get(),
                      self.retrieve_text(self.definition),
                      self.retrieve_text(self.additional_info),
                      0.0)
        self.db_manager.save_record(table_name, parameters)

    def retrieve_text(self, text_widget):
        return text_widget.get('1.0', 'end')

    def view_selected_item(self, item):
        current_item = self.table.focus()
        word = self.table.item(current_item)['text']
        for record in self.current_records:
            if record[0] == word:
                self.insert_to_definition(record[1])
                self.additional_info.delete('1.0', 'end')
                self.additional_info.insert('insert', record[2])


def main():
    view = View(controller.Controller())
    view.mainloop()


if __name__ == '__main__':
    main()
