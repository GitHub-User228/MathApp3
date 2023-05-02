

'''

'''
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class MainWindow(Screen):

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        properties_button = {'background_color': [36/255., 200/255., 22/255., 1.],
                             'background_normal': '',
                             'color': [100/255., 0/255., 140/255., 1.],
                             'font_size': 28,
                             'font_name': 'Century'}

        properties_input = {'background_color': [221 / 255., 221 / 255., 221 / 255., 1.],
                            'background_normal': '',
                            'foreground_color': [0/255., 0/255., 0/255., 1.],
                            'font_size': 32,
                            'font_name': 'Arial',
                            'halign': 'center'}

        properties_label = {'color': [255/255., 255/255., 255/255., 1.],
                            'font_size': 28,
                            'font_name': 'Comic Sans MS'}

        self.VerticalLayout = BoxLayout(orientation='vertical',
                                        spacing=20,
                                        padding=[10, 10, 10, 10])

        # Row 1
        self.Label1 = Label(text='Выбери тип задания', **properties_label)

        # Row 2
        self.TasksLayout = BoxLayout(orientation='horizontal', spacing=10)
        ## Col 1
        self.button_equations = Button(text='Уравнения', **properties_button)
        ## Col 2
        self.button_tasks = Button(text='Задачи', **properties_button)
        ## Adding widgets
        self.TasksLayout.add_widget(self.button_equations)
        self.TasksLayout.add_widget(self.button_tasks)

        # Row 3
        self.Label2 = Label(text='Выбери сложность', **properties_label)

        # Row 4
        self.ComplexityLayout = BoxLayout(orientation='horizontal', spacing=10)
        ## Col 1
        self.button_c_1 = Button(text='1', **properties_button)
        ## Col 2
        self.button_c_2 = Button(text='2', **properties_button)
        ## Col 3
        self.button_c_3 = Button(text='3', **properties_button)
        ## Col 4
        self.button_c_any = Button(text='Любая', **properties_button)
        ## Adding widgets
        self.ComplexityLayout.add_widget(self.button_c_1)
        self.ComplexityLayout.add_widget(self.button_c_2)
        self.ComplexityLayout.add_widget(self.button_c_3)
        self.ComplexityLayout.add_widget(self.button_c_any)

        # Row 5
        self.NumberOfTasksLayout = BoxLayout(orientation='horizontal', spacing=0)
        ## Col 1
        self.Label3 = Label(text='Кол-во заданий', **properties_label)
        ## Col 2
        self.TextInput_Ntasks = TextInput(text='5', multiline=False, **properties_input)
        ## Adding widgets
        self.NumberOfTasksLayout.add_widget(self.Label3)
        self.NumberOfTasksLayout.add_widget(self.TextInput_Ntasks)

        # Row 6
        self.MaxNumberLayout = BoxLayout(orientation='horizontal', spacing=0)
        ## Col 1
        self.Label4 = Label(text='Макс. число', **properties_label)
        ## Col 2
        self.Slider = Slider(orientation='horizontal', min=100, max=10000, value=100, step=100)
        self.Slider.fbind('value', self.update_slider_val)
        ## Col 3
        self.Label5_MaxNumber = Label(text=str(100), **properties_label)
        ## Adding widgets
        self.MaxNumberLayout.add_widget(self.Label4)
        self.MaxNumberLayout.add_widget(self.Slider)
        self.MaxNumberLayout.add_widget(self.Label5_MaxNumber)

        # Row 7
        self.MainLayout = BoxLayout(orientation='horizontal', spacing=10)
        ## Col 1
        self.button_start = Button(text='Старт', **properties_button)

        ## Col 2
        self.button_results = Button(text='Просмотреть результаты', **properties_button)
        ## Adding widgets
        self.MainLayout.add_widget(self.button_start)
        self.MainLayout.add_widget(self.button_results)

        # Adding Widgets

        self.VerticalLayout.add_widget(self.Label1)
        self.VerticalLayout.add_widget(self.TasksLayout)
        self.VerticalLayout.add_widget(self.Label2)
        self.VerticalLayout.add_widget(self.ComplexityLayout)
        self.VerticalLayout.add_widget(self.NumberOfTasksLayout)
        self.VerticalLayout.add_widget(self.MaxNumberLayout)
        self.VerticalLayout.add_widget(self.MainLayout)

        self.add_widget(self.VerticalLayout)

    def update_slider_val(self, instance, val):
        self.Label5_MaxNumber.text = str(int(val))


