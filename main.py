from kivy.config import Config

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '484')


from datetime import datetime

from kivy.app import App
from kivy.core.window import Window
from src.ui.MainWindow import MainWindow
from src.ui.TaskWindow import TaskWindow
from src.TasksGenerator import EquationsGenerator, TasksGenerator1
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock


def time_converter(dt):
    hours = int(dt // 3600)
    dt = dt - hours * 3600
    minutes = int(dt // 60)
    dt = dt - minutes * 60
    seconds = int(dt)
    if len(str(hours)) == 1: hours = f'0{hours}'
    if len(str(minutes)) == 1: minutes = f'0{minutes}'
    if len(str(seconds)) == 1: seconds = f'0{seconds}'
    return f'{hours}:{minutes}:{seconds}'


class Manager(ScreenManager):
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.complexity = 1
        self.number_of_tasks = 5
        self.max_number = None
        self.generator = EquationsGenerator()

        self.add_widget(MainWindow(name='menu'))
        self.add_widget(TaskWindow(name='task'))

        self.get_screen('menu').button_start.on_press = self.start
        self.get_screen('menu').button_equations.on_press = self.task_type_equations
        self.get_screen('menu').button_tasks.on_press = self.task_type_tasks
        self.get_screen('menu').button_c_1.on_press = self.set_complexity_1
        self.get_screen('menu').button_c_2.on_press = self.set_complexity_2
        self.get_screen('menu').button_c_3.on_press = self.set_complexity_3
        self.get_screen('menu').button_c_any.on_press = self.set_complexity_any

        self.tasks = None
        self.real_answers = None
        self.answers = None
        self.is_done = None
        self.counter = None
        self.start_time = None
        self.times = None
        self.clock = None

        self.get_screen('task').button.on_press = self.next_task

    def start(self):
        try:
            n_tasks = int(self.get_screen('menu').TextInput_Ntasks.text)
            if n_tasks < 1:
                self.get_screen('menu').TextInput_Ntasks.text = "Ошибка: введите число > 0"
            else:
                self.number_of_tasks = n_tasks
                self.max_number = int(self.get_screen('menu').Label5_MaxNumber.text)
                self.generator.reset(self.number_of_tasks, complexity=self.complexity, max_number=self.max_number)
                tasks, real_answers = self.generator.generate()
                self.reset_task_ui(tasks, real_answers)
                self.start_time = datetime.now()
                self.start_timer()
                self.current = 'task'
        except Exception as e:
            print(e)
            self.get_screen('menu').TextInput_Ntasks.text = "Ошибка: введите число > 0"

    def start_timer(self):
        self.clock = Clock.schedule_interval(self.update_timer, 1/30)

    def stop_timer(self):
        self.clock.cancel()

    def update_timer(self, dt):
        dt = time_converter((datetime.now() - self.start_time).total_seconds())
        self.get_screen('task').Label3_timer.text = dt

    def task_type_equations(self):
        self.generator = EquationsGenerator()

    def task_type_tasks(self):
        self.generator = TasksGenerator1()

    def set_complexity_1(self):
        self.complexity = 1

    def set_complexity_2(self):
        self.complexity = 2

    def set_complexity_3(self):
        self.complexity = 3

    def set_complexity_any(self):
        self.complexity = 'any'

    def reset_task_ui(self, tasks, real_answers):
        self.is_done = False
        self.answers = []
        self.times = []
        self.tasks = tasks
        self.real_answers = real_answers
        self.counter = 1
        self.get_screen('task').Label2_Task.text = self.tasks[0]
        self.get_screen('task').Label1_NTask.text = f"Задание {self.counter} из {self.number_of_tasks}"

    def next_task(self):
        if self.counter == self.number_of_tasks:
            try:
                ans = int(self.get_screen('task').TextInput.text)
                self.answers.append(ans)
                self.times.append(self.get_screen('task').Label3_timer.text)
                self.stop_timer()
                self.get_screen('task').TextInput.text = ""
                #self.results_window.update(ans, self.real_answers[self.counter-1], self.tasks[self.counter-1], self.dt.toString())
                self.counter += 1
                correct_answers = sum([True if self.answers[i] == self.real_answers[i] else False for i in
                                       range(self.number_of_tasks)])
                self.get_screen('task').Label2_Task.text = f"Ты решил все задания\nТвой результат: {correct_answers} из {self.number_of_tasks}"
                self.is_done = True
            except Exception as e:
                print(e)
                self.get_screen('task').TextInput.text = "Ошибка ввода"
        elif self.counter > self.number_of_tasks:
            pass
        else:
            try:
                ans = int(self.get_screen('task').TextInput.text)
                self.answers.append(ans)
                self.times.append(self.get_screen('task').Label3_timer.text)
                self.get_screen('task').TextInput.text = ""
                #self.results_window.update(ans, self.real_answers[self.counter-1], self.tasks[self.counter-1], self.dt.toString())
                self.counter += 1
                self.get_screen('task').Label1_NTask.text = f"Задание {self.counter} из {self.number_of_tasks}"
                self.get_screen('task').Label2_Task.text = self.tasks[self.counter-1]
            except Exception as e:
                print(e)
                self.get_screen('task').TextInput.text = "Ошибка ввода"

class MathTasks(App):
    def build(self):
        sm = Manager()
        Window.clearcolor = (139/255., 0/255., 203/255., 1)
        return sm


if __name__ in ('__main__', '__android__'):
    MathTasks().run()