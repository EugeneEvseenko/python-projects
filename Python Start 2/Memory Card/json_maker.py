import json
import os
class Question():
    ''' содержит вопрос, правильный ответ и три неправильных'''
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3
        self.passed = False
        self.quan = None

questions_list = [] 
questions_list.append(Question('Государственный язык Бразилии', 'Португальский', 'Английский', 'Испанский', 'Бразильский'))
questions_list.append(Question('Какого цвета нет на флаге России?', 'Зелёный', 'Красный', 'Белый', 'Синий'))
questions_list.append(Question('Национальная хижина якутов', 'Ураса', 'Юрта', 'Иглу', 'Хата'))
questions_list.append(Question('С какой из этих стран Чехия не граничит?', 'Венгрия', 'Австрия', 'Польша', 'Германия'))
questions_list.append(Question('Какая из этих кислот является витамином?', 'Никотиновая', 'Яблочная', 'Янтарная', 'Молочная'))
questions_list.append(Question('Какую икру больше всего любил Джеймс Бонд?', 'Белужью', 'Севрюжью', 'Стерляжью', 'Осетровую'))
questions_list.append(Question('Какой химический элемент был назван в честь злого подземного гнома?', 'Кобальт', 'Гафний', 'Бериллий', 'Теллур'))
questions_list.append(Question('Какого зайца НЕ бывает?', 'Чувак', 'Тумак', 'Русак', 'Беляк'))
questions_list.append(Question('Какая планета совершает 1 оборот вокруг солнца со скоростью 47,9 км/с', 'Меркурий', 'Марс', 'Юпитер', 'Сатурн'))
questions_list.append(Question('Чему равна сумма чисел от 0 до 100 включительно?', '5050', '3525', '1000', '7550'))
questions_list.append(Question('Какой буквой физики обозначают ускорение свободного падения?', 'g', 'f', 'n', 'm'))

'''
    Запаковать список классов невозможно, поэтому необходимо преобразовать 
    его в какую-нибудь структуру данных, например в список словарей.
'''
templist = []
for q in questions_list: # перебираем все вопросы
    templist.append( # формируем словарь и добавляем его в список
        {
            'question' : q.question,
            'right_answer' : q.right_answer,
            'wrong1' : q.wrong1,
            'wrong2' : q.wrong2,
            'wrong3' : q.wrong3
        }
    )
'''
    Сериализацей JSON занимается модуль json, поэтому перед
    использованием нужно его подключить.

    Функция open открывает файл с именем указанным в первом
    параметре, второй параматер отвечает за атрибук доступа
    w - перезапись(если файл существует, то в нем все данные удалятся)
    a - дозапись(если файл существует, то он будет дополнен)
    r - чтение.

    Параметр encoding отвечает за кодировку текста.

    ensure_ascii отвечает за использование кодировки ascii.
'''
TEST_NAME = 'Тест лол кек чебурек'
TEST_DIFF = 'Лёгкая'
outjson = {
    'name' : TEST_NAME, # имя
    'difficult' : TEST_DIFF, # сложность
    'questions' : templist # вопросы
}
if not os.path.exists('tests'): # проверка существования папки с тестами
    os.mkdir('tests') # если не существует, то создаём
json.dump(outjson, open(f"tests/{TEST_NAME}.json", "w", encoding="utf-8"), ensure_ascii=False)
