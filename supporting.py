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