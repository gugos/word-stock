from tkinter import Toplevel, Button, Text, Scrollbar, Entry, StringVar, Label, Frame
import tkinter.messagebox as tmb
from collections import namedtuple
from collections import OrderedDict
from random import shuffle
from difflib import SequenceMatcher
from result_view import ResultView

QUIZ_COUNT = 24


class QuizView(Toplevel):
    def __init__(self, db_manager):
        Toplevel.__init__(self)
        self.db_manager = db_manager
        self.quiz_list = []
        self.buttons_list = []
        self.saved_answers = {index: '' for index in range(0, QUIZ_COUNT)}
        self.generate_quiz()
        self.create_gui()
        self.quiz_counter = 0
        self.display_quiz()

    def create_gui(self):
        self.status_lable = Label(self, text=f'01 / {QUIZ_COUNT}')
        self.status_lable.grid(row=0, column=0, columnspan=4)
        self.definition = Text(self, wrap='word')
        self.definition.grid(row=1, column=0, columnspan=4)
        scrollbar = Scrollbar(self, command=self.definition.yview)
        scrollbar.grid(row=1, column=4, sticky='nsew')
        self.definition['yscrollcommand'] = scrollbar.set
        self.textvariable = StringVar()
        Entry(self, textvariable=self.textvariable, justify='center').grid(row=2, column=0, columnspan=4, sticky='nsew')
        self.button_prev = Button(self, text='<<<', command=lambda step=-1: self.change_quiz(step))
        self.button_prev.grid(row=3, column=0, sticky='nsew')
        self.button_next = Button(self, text='>>>', command=lambda step=1: self.change_quiz(step))
        self.button_next.grid(row=3, column=1, sticky='nsew')
        frame = Frame(self)
        frame.grid(row=3, column=2)
        row_count = 2
        column_count = 12
        for row in range(0, row_count):
            quiz_number = row * column_count
            for column in range(0, column_count):
                button = Button(frame, command=lambda number=quiz_number: self.select_quiz(number), background='grey')
                self.buttons_list.append(button)
                button.grid(row=row, column=column, sticky='nsew')
                quiz_number += 1
        self.finish_button = Button(self, text='Finish', command=self.on_finish_button_clicked)
        self.finish_button.grid(row=3, column=3, sticky='nsew')

    def generate_quiz(self):
        records = self.db_manager.get_records_count()
        if records < QUIZ_COUNT:
            tmb.showwarning('Warning', 'Not enough records in db_dictionary.\nAt least 25 records required.')
            return
        score_objects = self.create_score_objects()
        for name in score_objects:
            score = score_objects[name]
            if not score.records_count:
                continue
            if score.records_count <= score.limit or QUIZ_COUNT - score.limit >= records - score.records_count:
                self.quiz_list.extend(self.db_manager.get_all_records_by_score_range((score.start, score.end)))
            else:
                self.quiz_list.extend(self.db_manager.get_random_records_by_score_range((score.start, score.end, score.limit)))
            if len(self.quiz_list) >= QUIZ_COUNT:
                lst = self.quiz_list[:QUIZ_COUNT]
                print(len(lst))
                for item in lst:
                    print(item)
                shuffle(self.quiz_list)
                break

    def create_score_objects(self):
        score_objects = OrderedDict()
        Score = namedtuple('Score', ['name', 'start', 'end', 'limit', 'records_count'])
        score_values = self.get_score_default_values()
        for key in score_values:
            name = key
            start, end, limit = score_values[key]
            records_count = self.db_manager.get_records_count_by_score_range((start, end))
            score_objects[key] = Score(name, start, end, limit, records_count)
        return score_objects

    def get_score_default_values(self):
        return OrderedDict(
            F=(0, 39, 8),
            E=(40, 59, 6),
            D=(60, 69, 4),
            C=(70, 79, 3),
            B=(80, 89, 2),
            A=(90, 100, 1),
        )

    def on_finish_button_clicked(self):
        self.finish_button['state'] = 'disabled'
        self.save_answer()
        result_window = ResultView(['Answer', 'Word', 'After', 'Before'])
        result_window.resizable(False, False)
        total_score = 0.0
        for index in self.saved_answers:
            answer = self.saved_answers[index]
            word = self.quiz_list[index][0]
            table_name = word[0]
            score_after = SequenceMatcher(None, answer, word).ratio() * 100
            total_score += score_after
            score_before = self.quiz_list[index][2]
            result_window.add_to_result([answer, word, score_after, score_before])
            self.db_manager.update_score(table_name, word, score_after)
        avg_score = total_score / QUIZ_COUNT
        result_window.set_quiz_score(avg_score)

    def change_quiz(self, step):
        self.save_answer()
        self.quiz_counter += step
        self.display_quiz()
        self.update_status()

    def select_quiz(self, quiz_number):
        self.save_answer()
        self.quiz_counter = quiz_number
        self.display_quiz()
        self.update_status()

    def save_answer(self):
        answer = self.textvariable.get()
        if len(answer):
            self.highlight_button('green')
        else:
            self.highlight_button('grey')
        self.saved_answers[self.quiz_counter] = answer

    def update_status(self):
        current_counter = self.quiz_counter + 1
        if current_counter < 10:
            status_text = f'0{current_counter} / {QUIZ_COUNT}'
        else:
            status_text = f'{current_counter} / {QUIZ_COUNT}'
        self.status_lable.config(text=status_text)

    def display_quiz(self):
        if self.quiz_counter >= QUIZ_COUNT:
            self.quiz_counter = 0
        elif self.quiz_counter < 0:
            self.quiz_counter = QUIZ_COUNT - 1
        self.highlight_button('orange')
        self.textvariable.set(self.saved_answers[self.quiz_counter])
        self.definition.delete('1.0', 'end')
        self.definition.insert('insert', self.quiz_list[self.quiz_counter][1])

    def highlight_button(self, color):
        button = self.buttons_list[self.quiz_counter]
        button['bg'] = color
