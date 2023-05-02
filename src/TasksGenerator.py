import random
from itertools import chain
import operator

OPERATIONS = {"+": operator.add, "-": operator.sub, "*": operator.mul, ":": operator.ifloordiv}
VARIABLES = ['x', 'y', 'a', 'm', 'n', 'q', 't']
DIVS = lambda n: chain(*((d, n // d) for d in range(1, int(n ** 0.5) + 1) if n % d == 0))
MAX_NUMBER_GENERATED = 1000
MIN_NUMBER_GENERATED = 2
K = 1


class BaseGenerator():
    def __init__(self):
        self.Ntasks = None
        self.complexity = None
        self.max_number = None

    def reset(self, Ntasks, complexity, max_number):
        self.Ntasks = Ntasks
        self.complexity = complexity
        self.max_number = max_number

    def generate(self):
        tasks = []
        real_answers = []
        for k in range(self.Ntasks):
            task, ans = self.generate_single_task()
            tasks.append(task)
            real_answers.append(ans)
        return tasks, real_answers

    def generate_single_task(self):
        task = None
        ans = None
        return task, ans

    def validate_task(self, input):
        pass


class EquationsGenerator(BaseGenerator):

    def __init__(self):
        super().__init__()

    def generate_single_task(self):
        ans = random.randint(1, self.max_number)
        equation = ans
        task = VARIABLES[random.randint(0, len(VARIABLES) - 1)]
        while True:
            if self.complexity == 'Any':
                complexity = random.randint(1, 3)
            else:
                complexity = self.complexity
            for it in range(complexity):
                equation, task = self.step(equation, task)
                if not equation:
                    break
            if (it == complexity - 1) and (equation is not False):
                break
            equation = ans
            task = VARIABLES[random.randint(0, len(VARIABLES) - 1)]
        if (task[0] == '(') and (task[-1] == ')'):
            task = task[1:-1]
        task += ' = ' + str(equation['res'])
        return task, ans

    def step(self, prev_equation, prev_task):
        '''
        I order:
        x +/-/:/* a = b
        II order:
        (x +/-/:/* a) +/-/:/* b = c
        III order:
        ((x +/-/:/* a) +/-/:/* b) +/-/:/* c = d
        '''
        task = 'POS1 OPERATION POS2'
        equation = {'pos1': None, 'operation': None, 'pos2': None, 'res': None}
        operation = list(OPERATIONS.keys())[random.randint(0, 3)]
        task = task.replace('OPERATION', operation)
        equation['operation'] = operation
        posx = random.randint(1, 2)
        try:
            equation[f'pos{posx}'] = prev_equation['res']
            if ((operation in ['*', ':']) and (prev_equation['operation'] in ['*', ':'])) and (posx == 2):
                task = task.replace(f'POS{posx}', f'({prev_task})')
            else:
                task = task.replace(f'POS{posx}', f'{prev_task}')
            if operation in ['+', '-']:
                task = '(' + task + ')'
        except:
            equation[f'pos{posx}'] = prev_equation
            task = task.replace(f'POS{posx}', f'{prev_task}')
            if operation in ['+', '-']:
                task = '(' + task + ')'
        iter = 0
        while True:
            if operation == ':' and posx == 2:
                equation[f'pos{1 if posx == 2 else 2}'] = equation[f'pos{posx}'] * random.randint(MIN_NUMBER_GENERATED,
                                                                                                  max(MIN_NUMBER_GENERATED + 1,
                                                                                                      self.max_number //
                                                                                                      equation[
                                                                                                          f'pos{posx}']))
            elif operation == ':' and posx == 1:
                dividers = list(DIVS(equation[f'pos{posx}']))
                equation[f'pos{1 if posx == 2 else 2}'] = dividers[random.randint(0, len(dividers) - 1)]
            else:
                equation[f'pos{1 if posx == 2 else 2}'] = random.randint(MIN_NUMBER_GENERATED, self.max_number)
            equation['res'] = OPERATIONS[operation](equation['pos1'], equation['pos2'])
            iter += 1
            if self.validate_task(equation):
                task = task.replace(f'POS{1 if posx == 2 else 2}', str(equation[f'pos{1 if posx == 2 else 2}']))
                break
            if iter == 100:
                return False, None
        equation[f'pos{posx}'] = prev_equation
        return equation, task

    def validate_task(self, equation):
        if any([v < 1 for v in [equation['pos1'], equation['pos2'], equation['res']]]):
            return False
        elif any([v >= self.max_number * K for v in [equation['pos1'], equation['pos2'], equation['res']]]):
            return False
        return True


class TasksGenerator1(BaseGenerator):
    ACTIONS_FORMS = {'м': [('ть', 'л'), ('ся', 'ся')],
                     'ж': [('ть', 'ла'), ('ся', 'сь')]}
    BASE_TEMPLATE1 = 'ACTOR APPENDIX1 APPENDIX2 ACTION MAINPART. Q_VERB TARGET.'
    ACTOR = [(('Велосипедист', 'м', 1), {'ACTION': [0], 'APPENDIX1': [0], 'APPENDIX2': [0], 'MAINPART': [0, 1, 2]}),
             (('Водитель', 'м', 1), {'ACTION': [0], 'APPENDIX1': [0], 'APPENDIX2': [0], 'MAINPART': [0, 1, 2]}),
             (('Мотоциклист', 'м', 1), {'ACTION': [0], 'APPENDIX1': [0], 'APPENDIX2': [0], 'MAINPART': [0, 1, 2]}),
             (('Грузовик', 'м', 1), {'ACTION': [0], 'APPENDIX1': [0], 'APPENDIX2': [0], 'MAINPART': [0, 1, 2]}),
             (('Машина', 'ж', 1), {'ACTION': [0], 'APPENDIX1': [0], 'APPENDIX2': [0], 'MAINPART': [0, 1, 2]}),
             (('Поезд', 'м', 1), {'ACTION': [0], 'APPENDIX1': [0], 'APPENDIX2': [0], 'MAINPART': [0, 1, 2]}),
             (('Температура', 'ж', 4),
              {'ACTION': [1, 2, 3, 4, 5, 6], 'APPENDIX1': [0, 1, 2, 3, 4], 'APPENDIX2': [0], 'MAINPART': [3, 4, 5]}),
             (('Объем', 'м', 3),
              {'ACTION': [1, 2, 3, 4, 5, 6], 'APPENDIX1': [0, 1, 2, 3, 4], 'APPENDIX2': [0], 'MAINPART': [3, 4, 5]}),
             (('Площадь', 'ж', 2), {'ACTION': [4, 6], 'APPENDIX1': [5, 6], 'APPENDIX2': [0], 'MAINPART': [3, 4, 5]})]
    ACTION = ['проехать', 'подняться', 'опуститься', 'cнизиться', 'уменьшиться', 'повыситься', 'увеличиться']
    APPENDIX1 = ['', 'жидкости', 'воды', 'воздуха', 'газа',
                 'наводнения', "пожара"]
    APPENDIX2 = ['']
    MAINPART = [('S за T', 'скорость'),
                ('T со скоростью V', 'расстояние'),
                ('S со скоростью V', 'время'),
                ('на S за T', 'скорость изменения'),
                ('за T со скоростью изменения V', 'изменение'),
                ('на S со скоростью изменения V', 'время')]
    Q_VERB = ['Определите', 'Найдите', 'Вычислите']
    TERMS = ['S', 'T', 'V']

    UNITS_S = {1: (['мм', 'см', 'дм', 'м', 'км'], [[1, 0.1, 0.01, 0.001, 0.000001],
                                                     [10, 1, 0.1, 0.01, 0.00001],
                                                     [100, 10, 1, 0.1, 0.0001],
                                                     [1000, 100, 10, 1, 0.001],
                                                     [1000000, 100000, 10000, 1000, 1]]),
               2: (['$мм^{2}$', '$см^{2}$', '$дм^{2}$', '$м^{2}$', '$км^{2}$'],
                     [[1, 0.1 ** 2, 0.01 ** 2, 0.001 ** 2, 0.000001 ** 2],
                      [10 ** 2, 1, 0.1 ** 2, 0.01 ** 2, 0.00001 ** 2],
                      [100 ** 2, 10 ** 2, 1, 0.1 ** 2, 0.0001 ** 2],
                      [1000 ** 2, 100 ** 2, 10 ** 2, 1, 0.001 ** 2],
                      [1000000 ** 2, 100000 ** 2, 10000 ** 2, 1000 ** 2, 1]]),
               3: (['л'], [1]),
               4: (['°C'],[1])}
    UNITS_T = (['c', 'мин', 'ч'], [[1, 1 / 60, 1 / 3600],
                                   [60, 1, 1 / 60],
                                   [3600, 60, 1]])

    def __init__(self):
        super().__init__()

    def reset(self, Ntasks, complexity, max_number):
        self.Ntasks = Ntasks
        self.complexity = complexity
        self.max_number = max_number

    def generate(self):
        tasks = []
        real_answers = []
        for k in range(self.Ntasks):
            task, ans = self.generate_single_task()
            tasks.append(task)
            real_answers.append(ans)
        return tasks, real_answers

    def generate_single_task(self):
        terms = {'S': [None, None], 'V': [random.randint(1, int(self.max_number ** (0.5))), None],
                 'T': [random.randint(1, int(self.max_number ** (0.5))), None]}
        terms['S'][0] = terms['V'][0] * terms['T'][0]
        term = self.TERMS[random.randint(0, 2)]
        case = random.choice(self.ACTOR)
        terms = self.select_units(terms, case)

        kind = case[0][1]
        mainpart = random.choice([k for k in [self.MAINPART[j] for j in case[1]['MAINPART']] if term not in k[0]])

        task = self.BASE_TEMPLATE1[:]
        task = task.replace('ACTOR', case[0][0])
        action = random.choice([self.ACTION[k] for k in case[1]['ACTION']])

        action = action.replace(*self.ACTIONS_FORMS[kind][0])
        action = action.replace(*self.ACTIONS_FORMS[kind][1])
        task = task.replace('ACTION', action)
        task = task.replace('APPENDIX1', random.choice([self.APPENDIX1[k] for k in case[1]['APPENDIX1']]))
        task = task.replace('APPENDIX2', random.choice([self.APPENDIX2[k] for k in case[1]['APPENDIX2']]))
        task = task.replace('MAINPART', mainpart[0])
        task = task.replace('Q_VERB', random.choice(self.Q_VERB))
        task = task.replace('TARGET', mainpart[1])
        for t in [k for k in self.TERMS if k != term]:
            task = task.replace(t, f'{terms[t][0]} {terms[t][1]}')
        task = self.split_task(task)
        return task, terms[term]

    def select_units(self, terms, case):
        terms['T'][1] = random.choice(self.UNITS_T[0])
        terms['S'][1] = random.choice(self.UNITS_S[case[0][2]][0])
        terms['V'][1] = f"{terms['S'][1]}/{terms['T'][1]}"
        return terms

    def split_task(self, task):
        fs = 22
        width = 800
        symbols_per_line = width // fs
        words = task.split(' ')
        new_task = ''
        length = 0
        for it, word in enumerate(words):
            if (length + len(word)) >= symbols_per_line:
                new_task += '\n'
                length = 0
            new_task += word + ' '
            length += len(word) + 1
        new_task = new_task.replace('  ', ' ')
        return new_task
