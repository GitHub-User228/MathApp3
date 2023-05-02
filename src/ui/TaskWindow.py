from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget

class TaskWindow(Screen):

    def __init__(self, **kwargs):
        super(TaskWindow, self).__init__(**kwargs)

        properties_button = {'background_color': [36/255., 200/255., 22/255., 1.],
                             'background_normal': '',
                             'color': [100/255., 0/255., 140/255., 1.],
                             'font_size': 32,
                             'font_name': 'Century'}

        properties_input = {'background_color': [221 / 255., 221 / 255., 221 / 255., 1.],
                            'background_normal': '',
                            'foreground_color': [0/255., 0/255., 0/255., 1.],
                            'font_size': 32,
                            'font_name': 'Arial',
                            'halign': 'center'}

        properties_label = {'color': [255/255., 255/255., 255/255., 1.],
                            'font_size': 42,
                            'font_name': 'Comic Sans MS'}

        properties_task = {'background_color': [221 / 255., 221 / 255., 221 / 255., 1.],
                           'background_normal': '',
                           'font_size': 42,
                           'font_name': 'Century',
                           'halign': 'center'}

        self.VerticalLayout = GridLayout(rows=3, cols=1, spacing=0)

        # Row 1
        self.Layout1 = BoxLayout(orientation='horizontal', spacing=0, size_hint=(None, None), height=80, width=1000)
        ## Col 1
        self.Label1_NTask = Label(text='Задание 2 из 10', **properties_label)
        ## Col 2
        self.Label3_timer = Label(text='00:00:00', **properties_label)
        ## Adding widgets
        self.Layout1.add_widget(self.Label1_NTask)
        self.Layout1.add_widget(self.Label3_timer)

        # Row 2
        self.Label2_Task = TextInput(text='Текст\nзадания', multiline=True, disabled=True, **properties_task,
                                     size_hint=(None, None), height=484-80-80, width=1000)
        self.Label2_Task.padding_y = [(484-80-80) / 2.0 - (28 / 2.0) * len(self.Label2_Task._lines), 0]

        # Row 3
        self.Layout2 = BoxLayout(orientation='horizontal', spacing=0, size_hint=(None, None), height=80, width=1000)
        ## Col 1
        self.Label3 = Label(text='Ответ', **properties_label)
        ## Col 2
        self.TextInput = TextInput(multiline=False, **properties_input)
        self.TextInput.padding_y = [80 / 2.0 - (32 / 2.0), 0]
        ## Col 3
        self.button = Button(text='Ответить', **properties_button)
        ## Adding widgets
        self.Layout2.add_widget(self.Label3)
        self.Layout2.add_widget(self.TextInput)
        self.Layout2.add_widget(self.button)

        # Adding Widgets
        self.VerticalLayout.add_widget(self.Layout1)
        self.VerticalLayout.add_widget(self.Label2_Task)
        self.VerticalLayout.add_widget(self.Layout2)

        self.add_widget(self.VerticalLayout)