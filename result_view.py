from tkinter import Toplevel, Label, ttk, Scrollbar, Frame


class ResultView(Toplevel):
    def __init__(self, header):
        Toplevel.__init__(self)
        self.header = header
        self.create_gui()

    def create_gui(self):
        self.table = ttk.Treeview(self)
        self.table['columns'] = tuple(i for i in range(2, len(self.header) + 1))
        self.table.grid(row=0, column=0, sticky='nsew')
        scrollbar = Scrollbar(self, command=self.table.yview)
        scrollbar.grid(row=0, column=1, sticky='nsew')
        self.table['yscrollcommand'] = scrollbar.set
        self.table.heading(column='#0', text=self.header[0], anchor='w')
        for index in range(1, len(self.header)):
            self.table.heading(column=index + 1, text=self.header[index], anchor='w')
        frame = Frame(self)
        frame.grid(row=1, column=0)
        Label(frame, text='Quiz score:').grid(row=0, column=0)
        self.total = Label(frame)
        self.total.grid(row=0, column=1)

    def add_to_result(self, data):
        values = tuple(data[1:])
        self.table.insert('', 0, text=data[0], values=values)

    def set_quiz_score(self, score):
        self.total['text'] = f'{score}'
