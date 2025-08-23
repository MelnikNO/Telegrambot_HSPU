# Клавиатуры и кнопки

from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from constants import BUTTON_MENU, BACK_BUTTON, SURNAME_BUTTON, DEPARTMENT_BUTTON, DEGREE_BUTTON, NOT_FOUND


def exit_keyboard() -> ReplyKeyboardMarkup:
    """ Создает клавиатуру с выходом в главное меню """
    keyboard = [[BUTTON_MENU]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def create_back_menu_keyboard() -> ReplyKeyboardMarkup:
    """ Универсальная клавиатура с кнопками 'Назад' и 'Меню' """
    keyboard = [
        [BACK_BUTTON],
        [BUTTON_MENU]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def start_keyboard() -> ReplyKeyboardMarkup:
    """ Создает клавиатуру для выбора стартовой фильтрации. """
    keyboard = [[SURNAME_BUTTON, DEPARTMENT_BUTTON],
                [DEGREE_BUTTON]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def start_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для выбора стартовой фильтрации """
    inline_keyboard = [[InlineKeyboardButton("Полное ФИО", callback_data="full_name")]]
    return InlineKeyboardMarkup(inline_keyboard)


def fullname_keyboard_inline() -> ForceReply:
    """ Запрашивает ввод полного ФИО преподавателя при выборе "Полное ФИО" """
    return ForceReply(input_field_placeholder="Введите полное ФИО преподавателя...")


def surname_keyboard_inline() -> ForceReply:
    """ Запрашивает ввод фамилии при выборе параметра "По фамилии" """
    return ForceReply(input_field_placeholder="Введите фамилию...")


def choiceaftersurname_keyboard() -> ReplyKeyboardMarkup:
    """ Создает клавиатуру для выбора следующего критерия в фильтре "По фамилии" """
    keyboard = [
        [DEPARTMENT_BUTTON, DEGREE_BUTTON],
        [BACK_BUTTON, BUTTON_MENU]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def department_keyboard() -> ReplyKeyboardMarkup:
    """ Создает клавиатуру при выборе параметра "По кафедре" """
    keyboard = [
        ["Факультет", "Институт"],
        [NOT_FOUND],
        [BUTTON_MENU]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def department_fuculty_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для выбора факультета из списка """
    inline_keyboard = [
        [InlineKeyboardButton("Безопасность жизнедеятельности", callback_data="bzhd_faculty")],
        [InlineKeyboardButton("Биология", callback_data="b_faculty")],
        [InlineKeyboardButton("География", callback_data="g_faculty")],
        [InlineKeyboardButton("Математика", callback_data="math_faculty")],
        [InlineKeyboardButton("Филологический факультет", callback_data="filo_faculty")],
        [InlineKeyboardButton("Химия", callback_data="chemistry_faculty")],
        [InlineKeyboardButton("Юридический факультет", callback_data="ur_faculty")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def bzhd_fuculty_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для факультета безопасности жизнедеятельности (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="zdorov_faculty")],
        [InlineKeyboardButton("2", callback_data="medicine_faculty")],
        [InlineKeyboardButton("3", callback_data="methodteachbzhd_faculty")],
        [InlineKeyboardButton("4", callback_data="basicsbzR_faculty")],
        [InlineKeyboardButton("5", callback_data="soshsafety_faculty")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def biology_fuculty_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для факультета биологии (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="afchzh_faculty")],
        [InlineKeyboardButton("2", callback_data="boteko_faculty")],
        [InlineKeyboardButton("3", callback_data="zoogen_faculty")],
        [InlineKeyboardButton("4", callback_data="methodobbioeko_faculty")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def geograthy_fuculty_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для факультета географии (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="geogeo_faculty")],
        [InlineKeyboardButton("2", callback_data="methodgeokr_faculty")],
        [InlineKeyboardButton("3", callback_data="phizgeo_faculty")],
        [InlineKeyboardButton("4", callback_data="economygeo_faculty")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def math_fuculty_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для факультета математики (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="algebra_faculty")],
        [InlineKeyboardButton("2", callback_data="geometry_faculty")],
        [InlineKeyboardButton("3", callback_data="mathanali_faculty")],
        [InlineKeyboardButton("4", callback_data="methodmathinfo_faculty")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def philology_fuculty_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для филологического факультета (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="abroadbook_faculty")],
        [InlineKeyboardButton("2", callback_data="mezhcult_faculty")],
        [InlineKeyboardButton("3", callback_data="obrtechn_faculty")],
        [InlineKeyboardButton("4", callback_data="russianlang_faculty")],
        [InlineKeyboardButton("5", callback_data="russianbook_faculty")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def chemistry_fuculty_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для факультета химии (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="neorg_faculty")],
        [InlineKeyboardButton("2", callback_data="orgch_faculty")],
        [InlineKeyboardButton("3", callback_data="chemistreko_faculty")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def juridical_fuculty_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для юридического факультета (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="gos_faculty")],
        [InlineKeyboardButton("2", callback_data="grazhd_faculty")],
        [InlineKeyboardButton("3", callback_data="mezhpravo_faculty")],
        [InlineKeyboardButton("4", callback_data="theorypravogr_faculty")],
        [InlineKeyboardButton("5", callback_data="criminal_faculty")],
        [InlineKeyboardButton("6", callback_data="criminalprocess_faculty")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def department_institute_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для выбора института из списка """
    inline_keyboard = [
        [InlineKeyboardButton("Востоковедение", callback_data="east_institute")],
        [InlineKeyboardButton("Детство", callback_data="childhood_institute")],
        [InlineKeyboardButton("ИДОР", callback_data="idor_institute")],
        [InlineKeyboardButton("Иностранные языки", callback_data="lang_institute")],
        [InlineKeyboardButton("ИИТТО", callback_data="iitto_institute")],
        [InlineKeyboardButton("История и социальные науки", callback_data="history_institute")],
        [InlineKeyboardButton("Музыка, театр и хореография", callback_data="music_institute")],
        [InlineKeyboardButton("Народы Севера", callback_data="north_institute")],
        [InlineKeyboardButton("Педагогика", callback_data="teach_institute")],
        [InlineKeyboardButton("Психология", callback_data="psycho_institute")],
        [InlineKeyboardButton("Русский язык как иностранный", callback_data="Russia_institute")],
        [InlineKeyboardButton("Физика", callback_data="pthysics_institute")],
        [InlineKeyboardButton("Физическая культура и спорт", callback_data="sport_institute")],
        [InlineKeyboardButton("Философия человека", callback_data="fpeople_institute")],
        [InlineKeyboardButton("Художественное образование", callback_data="hudo_institute")],
        [InlineKeyboardButton("Экономика и управление", callback_data="economy_institute")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def east_institute_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для института востоковедения (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="east1_institute")],
        [InlineKeyboardButton("2", callback_data="east2_institute")],
        [InlineKeyboardButton("3", callback_data="east3_institute")],
        [InlineKeyboardButton("4", callback_data="east4_institute")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def childhood_institute_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для института детства (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="childhood1_institute")],
        [InlineKeyboardButton("2", callback_data="childhood2_institute")],
        [InlineKeyboardButton("3", callback_data="childhood3_institute")],
        [InlineKeyboardButton("4", callback_data="childhood4_institute")],
        [InlineKeyboardButton("5", callback_data="childhood5_institute")],
        [InlineKeyboardButton("6", callback_data="childhood6_institute")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def idor_institute_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для института дефектологического образования и реабилитации (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="idor1_institute")],
        [InlineKeyboardButton("2", callback_data="idor2_institute")],
        [InlineKeyboardButton("3", callback_data="idor3_institute")],
        [InlineKeyboardButton("4", callback_data="idor4_institute")],
        [InlineKeyboardButton("5", callback_data="idor5_institute")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def lang_institute_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для института иностранных языков (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="lang1_institute")],
        [InlineKeyboardButton("2", callback_data="lang2_institute")],
        [InlineKeyboardButton("3", callback_data="lang3_institute")],
        [InlineKeyboardButton("4", callback_data="lang4_institute")],
        [InlineKeyboardButton("5", callback_data="lang5_institute")],
        [InlineKeyboardButton("6", callback_data="lang6_institute")],
        [InlineKeyboardButton("7", callback_data="lang7_institute")],
        [InlineKeyboardButton("8", callback_data="lang8_institute")],
        [InlineKeyboardButton("9", callback_data="lang9_institute")],
        [InlineKeyboardButton("10", callback_data="lang10_institute")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def iitto_institute_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для института информационных технологий и технологического образования (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="iitto1_institute")],
        [InlineKeyboardButton("2", callback_data="iitto2_institute")],
        [InlineKeyboardButton("3", callback_data="iitto3_institute")],
        [InlineKeyboardButton("4", callback_data="iitto4_institute")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def history_institute_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для института истории и социальных наук (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="history1_institute")],
        [InlineKeyboardButton("2", callback_data="history2_institute")],
        [InlineKeyboardButton("3", callback_data="history3_institute")],
        [InlineKeyboardButton("4", callback_data="history4_institute")],
        [InlineKeyboardButton("5", callback_data="history5_institute")],
        [InlineKeyboardButton("6", callback_data="history6_institute")],
        [InlineKeyboardButton("7", callback_data="history7_institute")],
        [InlineKeyboardButton("8", callback_data="history8_institute")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def music_institute_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для института музыки, театра и хореографии (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="music1_institute")],
        [InlineKeyboardButton("2", callback_data="music2_institute")],
        [InlineKeyboardButton("3", callback_data="music3_institute")],
        [InlineKeyboardButton("4", callback_data="music4_institute")],
        [InlineKeyboardButton("5", callback_data="music5_institute")],
        [InlineKeyboardButton("6", callback_data="music6_institute")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def north_institute_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для института народов Севера (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="north1_institute")],
        [InlineKeyboardButton("2", callback_data="north2_institute")],
        [InlineKeyboardButton("3", callback_data="north3_institute")],
        [InlineKeyboardButton("4", callback_data="north4_institute")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def teach_institute_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для института педагогики (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="teach1_institute")],
        [InlineKeyboardButton("2", callback_data="teach2_institute")],
        [InlineKeyboardButton("3", callback_data="teach3_institute")],
        [InlineKeyboardButton("4", callback_data="teach4_institute")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def psycho_institute_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для института психологии (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="psycho1_institute")],
        [InlineKeyboardButton("2", callback_data="psycho2_institute")],
        [InlineKeyboardButton("3", callback_data="psycho3_institute")],
        [InlineKeyboardButton("4", callback_data="psycho4_institute")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def Russia_institute_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для института русского языка как иностранного (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="Russia1_institute")],
        [InlineKeyboardButton("2", callback_data="Russia2_institute")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def pthysics_institute_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для института физики (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="pthysics1_institute")],
        [InlineKeyboardButton("2", callback_data="pthysics2_institute")],
        [InlineKeyboardButton("3", callback_data="pthysics3_institute")],
        [InlineKeyboardButton("4", callback_data="pthysics4_institute")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def sport_institute_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для института физической культуры и спорта (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="sport1_institute")],
        [InlineKeyboardButton("2", callback_data="sport2_institute")],
        [InlineKeyboardButton("3", callback_data="sport3_institute")],
        [InlineKeyboardButton("4", callback_data="sport4_institute")],
        [InlineKeyboardButton("5", callback_data="sport5_institute")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def fpeople_institute_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для института философии человека (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="fpeople1_institute")],
        [InlineKeyboardButton("2", callback_data="fpeople2_institute")],
        [InlineKeyboardButton("3", callback_data="fpeople3_institute")],
        [InlineKeyboardButton("4", callback_data="fpeople4_institute")],
        [InlineKeyboardButton("5", callback_data="fpeople5_institute")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def hudo_institute_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для института художественного образования (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="hudo1_institute")],
        [InlineKeyboardButton("2", callback_data="hudo2_institute")],
        [InlineKeyboardButton("3", callback_data="hudo3_institute")],
        [InlineKeyboardButton("4", callback_data="hudo4_institute")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def economy_institute_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для института экономики и управления (цифры согласно представленному списку из кафедр) """
    inline_keyboard = [
        [InlineKeyboardButton("1", callback_data="economy1_institute")],
        [InlineKeyboardButton("2", callback_data="economy2_institute")],
        [InlineKeyboardButton("3", callback_data="economy3_institute")],
        [InlineKeyboardButton("4", callback_data="economy4_institute")],
        [InlineKeyboardButton("5", callback_data="economy5_institute")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def department_menu_keyboard() -> ReplyKeyboardMarkup:
    """ Клавиатура с кнопками после выбора кафедры """
    keyboard = [
        ["Вывод по всем"],
        ["Следующий фильтр"],
        [BACK_BUTTON],
        [BUTTON_MENU]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def create_numbered_keyboard(items, prefix):
    """ Создает инлайн-клавиатуру с кнопками в виде цифр (1, 2, 3...) для выбора конкретного преподавателя """
    keyboard = []
    for i, item in enumerate(items, 1):
        keyboard.append([InlineKeyboardButton(f"{i}. {item}", callback_data=f"{prefix}{i}")])
    return InlineKeyboardMarkup(keyboard)


def choiceafterdepartment_keyboard() -> ReplyKeyboardMarkup:
    """ Создает клавиатуру для выбора следующего критерия в фильтре "По кафедре" """
    keyboard = [
        [DEGREE_BUTTON],
        [BACK_BUTTON, BUTTON_MENU]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def degree_keyboard() -> ReplyKeyboardMarkup:
    """ Создает клавиатуру при выборе параметра "По ученой степени" """
    keyboard = [
        [NOT_FOUND],
        [BUTTON_MENU]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def degree_keyboard_inline() -> InlineKeyboardMarkup:
    """ Создает инлайн-клавиатуру для выбора ученой степени """
    inline_keyboard = [
        [InlineKeyboardButton("Кандидат наук", callback_data="candidat")],
        [InlineKeyboardButton("Доктор наук", callback_data="doctor")]
    ]
    return InlineKeyboardMarkup(inline_keyboard)


def choiceafterdegree_keyboard() -> ReplyKeyboardMarkup:
    """ Создает клавиатуру для выбора следующего критерия в фильтре "По ученой степени", если это был переход из главного меню """
    keyboard = [
        ["Вывод по всем"],
        [SURNAME_BUTTON, DEPARTMENT_BUTTON],
        [BACK_BUTTON, BUTTON_MENU]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def choiceafterdegreefromthelist_keyboard() -> ReplyKeyboardMarkup:
    """ Создает клавиатуру для выбора следующего действия в фильтре "По ученой степени", если это был переход из предыдущего фильтра """
    keyboard = [
        ["Вывод по всем"],
        [BACK_BUTTON, BUTTON_MENU]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)