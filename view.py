import controller
import tkinter as tk
import tkinter.messagebox as tmb
from tkinter import Tk, Text, Entry, Button, Label, Scrollbar


class View(Tk):
	def __init__(self, controller):
		Tk.__init__(self)
		self.definition = Text(self, wrap='word', state='disabled')
		self.additional_info = Text(self, wrap='word')
		self.textvariable = tk.StringVar()
		self.controller = controller
		self.create_gui()
		self.resizable(False, False)

	def create_gui(self):
		Label(self, text='Find word definition:').grid(row=0, sticky='w')
		Entry(self, textvariable=self.textvariable).grid(row=1, column=0, sticky='nwes')
		self.grid_columnconfigure(0, weight=1)
		Button(self, text='Find', command=self.on_button_find_clicked).grid(row=1, column=1, columnspan=2, sticky='nwes')
		Label(self, text='Definition:').grid(row=2, column=0, sticky='w')
		self.create_text_widget(self.definition, row=3, column=0, columnspan=2)
		Label(self, text='Additional information:').grid(row=4, column=0, sticky='w')
		self.create_text_widget(self.additional_info, row=5, column=0, columnspan=2)

	def create_text_widget(self, text_widget, row=0, column=0, columnspan=0):
		text_widget.grid(row=row, column=column, columnspan=columnspan)
		scrollbar = Scrollbar(self, command=text_widget.yview)
		scrollbar_column = columnspan
		scrollbar.grid(row=row, column=scrollbar_column, sticky='nsew')
		text_widget['yscrollcommand'] = scrollbar.set

	def on_button_find_clicked(self):
		self.definition.config(state='normal')
		self.definition.delete('1.0', 'end')
		word = self.textvariable.get()
		if not word:
			tmb.showwarning('Warning', 'Word entry is empty')
			self.definition.config(state='disabled')
			return
		status, result = self.controller.get_word_definition(word)
		if status:
			for word_type in result:
				self.definition.insert(tk.INSERT, word_type + '\n')
				for num, text in enumerate(result[word_type], 1):
					self.definition.insert(tk.INSERT, f'{num}) {text}\n')
		else:
			tmb.showerror('Error', result)
		self.definition.config(state='disabled')


def main():
	view = View(controller.Controller())
	view.mainloop()


if __name__ == '__main__':
	main()
