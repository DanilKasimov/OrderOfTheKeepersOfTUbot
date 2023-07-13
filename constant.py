import os
import DataBaseUtils

media_file_path = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media')) + '\\'
db = DataBaseUtils.DbConnection('OrderBot.db')

main_menu_buttons = {
    'Гороскоп по ЗЗ': 'horoscope',
    'Послать нахуй': 'fuck_you',
    'Объявить мышью': 'set_mouse',
    'Сделать комплимент': 'complement',
    'Дать леща': 'lesh',
    'Статистика': 'statistic',
    'Пожелать здоровья': 'pain',
    'Порча на понос': 'porch',
    'Пользователь заебал': 'zaeb',
}
users_dop = [
    'Бухгалтерия', 
    'Аудиторы',
    'Мониторинг',
    'Бит',
    'Миша',
    'Вонючая магистраль',
    'BPMS',
    'Инвентаризация',
    'Бабка уборщица',
    'Пиошники',
    'SAP',
    'Олег',
]