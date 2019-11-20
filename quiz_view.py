from tkinter import Toplevel, Button, Text, Scrollbar, Entry, StringVar, Label, Frame
from collections import namedtuple
from collections import OrderedDict
from random import shuffle
from difflib import SequenceMatcher
from result_view import ResultView
import csv
import score_grade_system as SGS


class QuizView(Toplevel):
    def __init__(self, db_manager):
        Toplevel.__init__(self)
        self.db_manager = db_manager
        self.quiz_count = SGS.TOTAL
        self.quiz_list = []
        self.buttons_list = []
        self.saved_answers = {index: '' for index in range(0, self.quiz_count)}
        self.generate_quiz()
        self.create_gui()
        self.current_quiz_number = 0
        self.display_quiz()

    def create_gui(self):
        self.status_lable = Label(self, text=f'01 / {self.quiz_count}')
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
        score_objects = self.create_score_objects()
        for name in score_objects:
            score = score_objects[name]
            if not score.records_count:
                continue
            if score.records_count <= score.limit or self.quiz_count - score.limit >= records - score.records_count:
                self.quiz_list.extend(self.db_manager.get_all_records_by_score_range((score.start, score.end)))
            else:
                self.quiz_list.extend(self.db_manager.get_random_records_by_score_range((score.start, score.end, score.limit)))
            if len(self.quiz_list) >= self.quiz_count:
                del self.quiz_list[self.quiz_count:]
                shuffle(self.quiz_list)
                break
        return True

    def create_score_objects(self):
        score_objects = OrderedDict()
        Score = namedtuple('Score', ['name', 'start', 'end', 'limit', 'records_count'])
        score_values = SGS.get_score_grade_system()
        for key in score_values:
            name = key
            start, end, limit = score_values[key]
            records_count = self.db_manager.get_records_count_by_score_range((start, end))
            score_objects[key] = Score(name, start, end, limit, records_count)
        return score_objects

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
        avg_score = total_score / self.quiz_count
        result_window.set_quiz_score(avg_score)
        with open('statistics.csv', mode='a') as stat_file:
            stat_writer = csv.writer(stat_file)
            stat_writer.writerow([str(avg_score)])

    def change_quiz(self, step):
        self.save_answer()
        self.current_quiz_number += step
        self.display_quiz()
        self.update_status()

    def select_quiz(self, quiz_number):
        self.save_answer()
        self.current_quiz_number = quiz_number
        self.display_quiz()
        self.update_status()

    def save_answer(self):
        answer = self.textvariable.get()
        if len(answer):
            self.highlight_button('green')
        else:
            self.highlight_button('grey')
        self.saved_answers[self.current_quiz_number] = answer

    def update_status(self):
        current_counter = self.current_quiz_number + 1
        if current_counter < 10:
            status_text = f'0{current_counter} / {self.quiz_count}'
        else:
            status_text = f'{current_counter} / {self.quiz_count}'
        self.status_lable.config(text=status_text)

    def display_quiz(self):
        if self.current_quiz_number >= self.quiz_count:
            self.current_quiz_number = 0
        elif self.current_quiz_number < 0:
            self.current_quiz_number = self.quiz_count - 1
        self.highlight_button('orange')
        self.textvariable.set(self.saved_answers[self.current_quiz_number])
        self.definition.delete('1.0', 'end')
        self.definition.insert('insert', self.quiz_list[self.current_quiz_number][1])

    def highlight_button(self, color):
        button = self.buttons_list[self.current_quiz_number]
        button['bg'] = color
