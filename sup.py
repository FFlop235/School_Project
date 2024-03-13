from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ContentType
from parcer import sign_in, con, table_parcer
from parcer import Grafic
from DataBase import select_user_data


btn_chemist = InlineKeyboardButton('Химия', callback_data='chemist')
btn_history = InlineKeyboardButton('История', callback_data='history')
btn_phisics = InlineKeyboardButton('Физика', callback_data='phisics')
btn_rus_language = InlineKeyboardButton('Русский язык', callback_data='rus_language')
btn_eng_language = InlineKeyboardButton('Английский язык', callback_data='eng_language')
btn_inf = InlineKeyboardButton('Информатика', callback_data='inf')
btn_geometry = InlineKeyboardButton('Геометрия', callback_data='geometry')
btn_literature = InlineKeyboardButton('Литература', callback_data='literature')
btn_technolagy = InlineKeyboardButton('Технология', callback_data='technolagy')
btn_biology = InlineKeyboardButton('Биология', callback_data='biology')
btn_geografy = InlineKeyboardButton('География', callback_data='geografy')
btn_soc_science = InlineKeyboardButton('Обществознание', callback_data='soc_science')
btn_BOLS = InlineKeyboardButton('ОБЖ', callback_data='BOLS')
btn_PC = InlineKeyboardButton("Физкультура", callback_data='PC')
btn_algebra = InlineKeyboardButton("Алгебра", callback_data='algebra')
kb_subject = InlineKeyboardMarkup().add(btn_chemist).add(btn_history).add(btn_phisics).add(btn_rus_language).add(btn_eng_language).add(btn_inf).add(btn_geometry).add(btn_literature).add(btn_technolagy).add(btn_biology).add(btn_geografy).add(btn_soc_science).add(btn_BOLS).add(btn_PC).add(btn_algebra).add(btn_algebra)

def return_num_subject(subject_name: str) -> int:
    match subject_name:
        case 'Индивидуальный проект':
            return 0
        case 'Иностранный язык ':
            return 1
        case 'Литература':
            return 2
        case 'Русский язык':
            return 3
        case 'Алгебра':
            return 4
        case 'Геометрия':
            return 5
        case 'Информатика':
            return 6
        case 'Технология':
            return 7
        case 'Биология':
            return 8
        case 'География':
            return 9
        case 'Физика':
            return 10
        case 'Химия':
            return 11
        case 'История':
            return 12
        case 'Обществознание':
            return 13
        case 'ОБЖ':
            return 14
        case 'Физическая культура':
            return 15
        
def return_quarter(quarter_num: int):
    match quarter_num:
        case 1:
            return 'Сентябрь', 'Октябрь'
        case 2:
            return 'Ноябрь', 'Декабрь'
        case 3:
            return 'Январь', 'Февраль', 'Март'
        case 4:
            return 'Март', 'Апрель', 'Май'

def return_quarter_name(quarter_num: int):
    match quarter_num:
        case 1:
            return "I"
        case 2:
            return "II"
        case 3:
            return "III"
        case 4:
            return "IV"
        
        case _:
            raise ValueError("Неправильная четверть!")

class CreateFile:
    def __init__(self, user: list, quarter: int, subject_name: str, filename: str):
        self.user = user
        self.quarter = quarter
        self.subject_name = subject_name
        self.filename = filename
    
    def create_image(self):
        sign_in(self.user[0], self.user[1], 'МБОУ "СОШ № 6"')
        con(self.quarter)
        if self.quarter <= 2:
            grf = Grafic(name=f'Оценки по {self.subject_name} за {return_quarter_name(self.quarter)} четверть', table_marks=table_parcer(), num_subject=return_num_subject(self.subject_name), f_mounth_name=return_quarter(self.quarter)[0], s_mounth_name=return_quarter(self.quarter)[1])
            f, s = grf.table_filter()
            grf.save_image(filename=self.filename, figure=grf.create_grafic(f, s))
        else:
            grf = Grafic(name=f'Оценки по {self.subject_name} за {return_quarter_name(self.quarter)} четверть', table_marks=table_parcer(), num_subject=return_num_subject(self.subject_name), f_mounth_name=return_quarter(self.quarter)[0], s_mounth_name=return_quarter(self.quarter)[1], t_mounth_name=return_quarter(self.quarter)[2])
            f, s, t = grf.table_filter()
            grf.save_image(filename=self.filename, figure=grf.create_grafic(f, s, t))


class SendFile:
    def __init__(self, id: int, quarter: int, subject: str):
        self.id = id
        self.quarter = quarter
        self.subject = subject



if __name__ == '__main__':
    f1 = CreateFile(select_user_data(855924622), 3, 'Химия', 'test2.png')
    f1.create_image()