# Обработчик команд

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
import csv
from fuzzywuzzy import fuzz
from states import FULLNAME, SURNAME, DEPARTMENT, DEGREE

from constants import START_MESSAGE, MENU_MASSAGE, FULLNAME, CSV_FILE, NO_RESULTS_MESSAGE, MSG_TEMPLATE, EXIT, SURNAME, SURNAME_RESULT, DEPARTMENT_TEXT
import keyboards
import logging
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """ Обработка команды /start """
    reset_search_context(context)
    combined_message = f"{START_MESSAGE}\n\n{MENU_MASSAGE}"
    update.message.reply_text(
        combined_message,
        reply_markup=keyboards.start_keyboard_inline(),
        parse_mode='HTML'
    )

    update.message.reply_text(
        "Выберите вариант поиска:",
        reply_markup=keyboards.start_keyboard()
    )

    return ConversationHandler.END


def show_menu(update: Update, context: CallbackContext) -> None:
    """ Показ главного меню """
    reset_search_context(context)

    if update.message:
        update.message.reply_text(
            text="Выберите вариант поиска:",
            reply_markup=keyboards.start_keyboard()
        )
        update.message.reply_text(
            MENU_MASSAGE,
            reply_markup=keyboards.start_keyboard_inline()
        )
    elif update.callback_query:
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text="Выберите вариант поиска:",
            reply_markup=keyboards.start_keyboard_inline()
        )

    return ConversationHandler.END


def choicefullname(update: Update, context: CallbackContext) -> int:
    """ Выбор инлайн-кнопки "Полное ФИО" """
    if update.callback_query:
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat_id
        context.bot.send_message(
            chat_id=chat_id,
            text=FULLNAME,
            reply_markup=keyboards.fullname_keyboard_inline()
        )
        context.bot.send_message(
            chat_id=chat_id,
            text=EXIT,
            reply_markup=keyboards.exit_keyboard()
        )
    else:
        update.message.reply_text(
            FULLNAME,
            reply_markup=keyboards.fullname_keyboard_inline()
        )
        update.message.reply_text(
            EXIT,
            reply_markup=keyboards.exit_keyboard()
        )

    context.user_data['waiting_for_fullname'] = True
    return FULLNAME


def process_fullname_input(update: Update, context: CallbackContext) -> int:
    """ Обработка введенного полного ФИО и поиск в CSV """
    fullname = update.message.text.strip()
    professors = []

    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                search_words = fullname.lower().split()
                row_words = row['name'].lower().split()
                if all(word in row_words for word in search_words):
                    professors.append(row)

        if not professors:
            update.message.reply_text(
                NO_RESULTS_MESSAGE,
                reply_markup=keyboards.create_back_menu_keyboard()
            )
        else:
            if len(professors) > 1:
                update.message.reply_text(
                    f"Найдено преподавателей: {len(professors)}\n",
                    reply_markup=keyboards.exit_keyboard()
                )
            for prof in professors:
                formatted_msg = MSG_TEMPLATE.format(
                    name=prof['name'],
                    degree=prof['degree'],
                    phone=prof['phone'],
                    email=prof['email'],
                    department=prof['department'],
                    url=prof['url']
                )

                update.message.reply_text(
                    formatted_msg,
                    reply_markup=keyboards.exit_keyboard(),
                    parse_mode='HTML',
                    disable_web_page_preview=True
                )

    except FileNotFoundError:
        update.message.reply_text(
            "Ошибка: файл с данными не найден",
            reply_markup=keyboards.create_back_menu_keyboard()
        )
    except Exception as e:
        update.message.reply_text(
            f"Произошла ошибка: {str(e)}",
            reply_markup=keyboards.create_back_menu_keyboard()
        )

    return ConversationHandler.END


def choicesurname(update: Update, context: CallbackContext) -> int:
    """ Выбор кнопки "По фамилии" """
    if update.callback_query:
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat_id
        context.bot.send_message(
            chat_id=chat_id,
            text=SURNAME,
            reply_markup=keyboards.surname_keyboard_inline()
        )
        context.bot.send_message(
            chat_id=chat_id,
            text=EXIT,
            reply_markup=keyboards.exit_keyboard()
        )
    else:
        update.message.reply_text(
            SURNAME,
            reply_markup=keyboards.surname_keyboard_inline()
        )
        update.message.reply_text(
            EXIT,
            reply_markup=keyboards.exit_keyboard()
        )

    context.user_data['waiting_for_surname'] = True
    return SURNAME


def process_surname_input(update: Update, context: CallbackContext) -> int:
    """ Обработка введенной фамилии и поиск в CSV или списке """
    surname = update.message.text.strip().lower()
    exact_matches = []
    similar_matches = []

    try:
        if 'current_professors' in context.user_data and context.user_data['current_professors']:
            source_list = context.user_data['current_professors']

            for prof in source_list:
                prof_name = prof['name'].lower()
                prof_surname = prof_name.split()[0]

                # Точное совпадение
                if prof_surname == surname:
                    exact_matches.append(prof)
                # Нечеткое сравнение
                elif fuzz.ratio(prof_surname, surname) > 80:
                    similar_matches.append(prof)
        else:
            with open(CSV_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    row_name = row['name'].lower()
                    row_surname = row_name.split()[0]

                    # Точное совпадение
                    if row_surname == surname:
                        exact_matches.append(row)
                    # Нечеткое сравнение
                    elif fuzz.ratio(row_surname, surname) > 80:
                        similar_matches.append(row)

        professors = exact_matches + similar_matches

        context.user_data['current_professors'] = professors
        context.user_data['current_search_type'] = 'surname'
        context.user_data['current_search_term'] = surname

        if not professors:
            update.message.reply_text(
                NO_RESULTS_MESSAGE,
                reply_markup=keyboards.create_back_menu_keyboard()
            )
            return ConversationHandler.END

        # Определение, был ли это первоначальный поиск или фильтрация
        is_initial_search = 'is_filtered_search' not in context.user_data or not context.user_data.get('is_filtered_search', False)

        # Информация о результатах поиска
        if exact_matches and similar_matches:
            result_message = (
                f"Точных совпадений: {len(exact_matches)}\n"
                f"Похожих фамилий: {len(similar_matches)}"
            )
        else:
            result_message = SURNAME_RESULT.format(count=len(professors))

        if is_initial_search:
            update.message.reply_text(
                result_message,
                reply_markup=keyboards.choiceaftersurname_keyboard()
            )
            context.user_data['is_filtered_search'] = False
        else:
            # Фильтрация по существующему списку
            update.message.reply_text(
                result_message,
                reply_markup=keyboards.choiceaftersurname_keyboard()
            )
            context.user_data['is_filtered_search'] = True

        # Вывод результатов
        for prof in professors:
            formatted_msg = MSG_TEMPLATE.format(
                name=prof['name'],
                degree=prof['degree'],
                phone=prof['phone'],
                email=prof['email'],
                department=prof['department'],
                url=prof['url']
            )

            update.message.reply_text(
                formatted_msg,
                reply_markup=keyboards.exit_keyboard(),
                parse_mode='HTML',
                disable_web_page_preview=True
            )

    except FileNotFoundError:
        update.message.reply_text(
            "Ошибка: файл с данными не найден",
            reply_markup=keyboards.create_back_menu_keyboard()
        )
    except Exception as e:
        update.message.reply_text(
            f"Произошла ошибка: {str(e)}",
            reply_markup=keyboards.create_back_menu_keyboard()
        )

    return ConversationHandler.END


def show_all_professors(update: Update, context: CallbackContext) -> None:
    """ Обработка кнопки 'Вывести всех' при выборе 'По фамилии' """
    if 'current_professors' not in context.user_data:
        update.message.reply_text(
            "Результаты поиска не найдены. Пожалуйста, выполните поиск заново.",
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return

    for prof in context.user_data['current_professors']:
        update.message.reply_text(
            MSG_TEMPLATE.format(
                name=prof['name'],
                degree=prof['degree'],
                phone=prof['phone'],
                email=prof['email'],
                department=prof['department'],
                url=prof['url']
            ),
            parse_mode='HTML',
            reply_markup=keyboards.exit_keyboard(),
            disable_web_page_preview=True
        )


def choicedepartment(update: Update, context: CallbackContext) -> int:
    """ Выбор кнопки "По кафедре" """
    if update.callback_query:
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat_id
        context.bot.send_message(
            chat_id=chat_id,
            text=DEPARTMENT_TEXT,
            reply_markup=keyboards.department_keyboard()
        )
    else:
        update.message.reply_text(
            DEPARTMENT_TEXT,
            reply_markup=keyboards.department_keyboard()
        )

    return DEPARTMENT


def handle_department_type(update: Update, context: CallbackContext) -> int:
    """ Обработка выбора типа подразделения (Факультет/Институт/Не указано) """
    text = update.message.text
    logger.info(f"handle_department_type вызвана с текстом: {text}")

    if text == "Факультет":
        logger.info("Пользователь выбрал Факультет")
        update.message.reply_text(
            "Выберите факультет:",
            reply_markup=keyboards.department_fuculty_keyboard_inline()
        )
        update.message.reply_text(
            "Вы можете также вернуться назад или в меню.",
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return DEPARTMENT

    elif text == "Институт":
        logger.info("Пользователь выбрал Институт")
        update.message.reply_text(
            "Выберите институт:",
            reply_markup=keyboards.department_institute_keyboard_inline()
        )
        update.message.reply_text(
            "Вы можете также вернуться назад или в меню.",
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return DEPARTMENT

    elif text == "Не указано":
        logger.info("Пользователь выбрал Не указано")
        professors = search_professors_without_department(context)

        context.user_data['current_professors'] = professors
        context.user_data['current_department'] = "Не указано"

        if professors:
            count_message = f"Найдено преподавателей: {len(professors)}"
            update.message.reply_text(
                count_message,
                reply_markup=keyboards.department_menu_keyboard()
            )
        else:
            update.message.reply_text(
                "Преподаватели без указанной кафедры не найдены",
                reply_markup=keyboards.create_back_menu_keyboard()
            )
        return DEPARTMENT

    else:
        logger.warning(f"Неизвестный выбор: {text}")
        update.message.reply_text(
            "Пожалуйста, выберите вариант из меню.",
            reply_markup=keyboards.department_keyboard()
        )
        return DEPARTMENT

    return DEPARTMENT


def search_professors_without_department(context: CallbackContext) -> list:
    """ Поиск преподавателей без указанной кафедры """
    professors = []
    if 'current_professors' in context.user_data:
        for prof in context.user_data['current_professors']:
            department = prof.get('department', '').lower().strip()
            if not department or "не указано" in department:
                professors.append(prof)
    else:
        try:
            with open(CSV_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if not row['department'].strip() or "не указано" in row['department']:
                        professors.append(row)
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
    return professors


def handle_faculty_selection(update: Update, context: CallbackContext) -> None:
    """ Обработка выбора факультета и кафедры """
    query = update.callback_query
    query.answer()

    faculty_code = query.data
    logger.info(f"Выбран факультет: {faculty_code}")

    context.user_data['current_faculty'] = faculty_code

    faculty_descriptions = {
        "bzhd_faculty": {
            "name": "Безопасность жизнедеятельности",
            "departments": [
                "1. Кафедра здоровьесбережения и основ медицинских знаний",
                "2. Кафедра медико-валеологических дисциплин",
                "3. Кафедра методики обучения безопасности жизнедеятельности",
                "4. Кафедра основы безопасности и защиты Родины",
                "5. Кафедра социальной безопасности"
            ]
        },
        "b_faculty": {
            "name": "Биология",
            "departments": [
                "1. Кафедра анатомии и физиологии человека и животных",
                "2. Кафедра ботаники и экологии",
                "3. Кафедра зоологии и генетики",
                "4. Кафедра методики обучения биологии и экологии"
            ]
        },
        "g_faculty": {
            "name": "География",
            "departments": [
                "1. Кафедра геологии и геоэкологии",
                "2. Кафедра методики обучения географии и краеведению",
                "3. Кафедра физической географии и природопользования",
                "4. Кафедра экономической географии"
            ]
        },
        "math_faculty": {
            "name": "Математика",
            "departments": [
                "1. Кафедра алгебры",
                "2. Кафедра геометрии",
                "3. Кафедра математического анализа",
                "4. Кафедра методики обучения математике и информатике"
            ]
        },
        "filo_faculty": {
            "name": "Филологический факультет",
            "departments": [
                "1. Кафедра зарубежной литературы",
                "2. Кафедра межкультурной коммуникации",
                "3. Кафедра образовательных технологий в филологии",
                "4. Кафедра русского языка",
                "5. Кафедра русской литературы"
            ]
        },
        "chemistry_faculty": {
            "name": "Химия",
            "departments": [
                "1. Кафедра неорганической химии",
                "2. Кафедра органической химии",
                "3. Кафедра химического и экологического образования"
            ]
        },
        "ur_faculty": {
            "name": "Юридический факультет",
            "departments": [
                "1. Кафедра государственного права",
                "2. Кафедра гражданского права",
                "3. Кафедра международного права",
                "4. Кафедра теории права и гражданско-правового образования",
                "5. Кафедра уголовного права",
                "6. Кафедра уголовного процесса"
            ]
        }
    }

    faculty_data = faculty_descriptions.get(faculty_code)
    if faculty_data:
        departments_text = "\n".join(faculty_data["departments"])
        message = (
            f"Факультет: {faculty_data['name']}\n\n"
            f"Доступные кафедры:\n{departments_text}\n\n"
        )

        context.bot.send_message(
            chat_id=query.message.chat_id,
            text=message,
            reply_markup=keyboards.create_back_menu_keyboard()
        )

    if faculty_code == "bzhd_faculty":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру факультета Безопасность жизнедеятельности:",
            reply_markup=keyboards.bzhd_fuculty_keyboard_inline()
        )
    elif faculty_code == "b_faculty":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру факультета Биология:",
            reply_markup=keyboards.biology_fuculty_keyboard_inline()
        )
    elif faculty_code == "g_faculty":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру факультета География:",
            reply_markup=keyboards.geograthy_fuculty_keyboard_inline()
        )
    elif faculty_code == "math_faculty":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру факультета Математика:",
            reply_markup=keyboards.math_fuculty_keyboard_inline()
        )
    elif faculty_code == "filo_faculty":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру факультета Филологический:",
            reply_markup=keyboards.philology_fuculty_keyboard_inline()
        )
    elif faculty_code == "chemistry_faculty":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру факультета Химия:",
            reply_markup=keyboards.chemistry_fuculty_keyboard_inline()
        )
    elif faculty_code == "ur_faculty":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру факультета Юридический:",
            reply_markup=keyboards.juridical_fuculty_keyboard_inline()
        )

    return DEPARTMENT


def handle_institute_selection(update: Update, context: CallbackContext) -> None:
    """ Обработка выбора институт """
    query = update.callback_query
    query.answer()

    institute_code = query.data
    logger.info(f"Выбран институт: {institute_code}")

    context.user_data['current_faculty'] = institute_code

    institute_descriptions = {
        "east_institute": {
            "name": "Востоковедение",
            "departments": [
                "1. Кафедра восточных языков и лингводидактики",
                "2. Кафедра древневосточных языков",
                "3. Кафедра китайской филологии",
                "4. Кафедра языков и культур исламского мира"
            ]
        },
        "childhood_institute": {
            "name": "Детство",
            "departments": [
                "1. Кафедра возрастной психологии и педагогики семьи",
                "2. Кафедра дошкольной педагогики",
                "3. Кафедра начального естественно-математического образования",
                "4. Кафедра педагогики начального образования и художественногого развития ребенка",
                "5. Кафедра раннего обучения иностранным языкам",
                "6. Кафедра языкового и литературного образования ребенка"
            ]
        },
        "idor_institute": {
            "name": "Институт дефектологического образования и реабилитации",
            "departments": [
                "1. Кафедра логопедии",
                "2. Кафедра олигофренопедагогики",
                "3. Кафедра основ дефектологии и реабилитологии",
                "4. Кафедра сурдопедагогики",
                "5. Кафедра тифлопедагогики"
            ]
        },
        "lang_institute": {
            "name": "Иностранные языки",
            "departments": [
                "1. Кафедра английского языка для профессиональной коммуникации",
                "2. Кафедра английского языка и лингвострановедения",
                "3. Кафедра английской филологии",
                "4. Кафедра интенсивного обучения иностранным языкам",
                "5. Кафедра методики обучения иностранным языкам",
                "6. Кафедра немецкого и романских языков для профессиональной коммуникации",
                "7. Кафедра немецкой филологии",
                "8. Кафедра перевода",
                "9. Кафедра романской филологии",
                "10. Кафедра языков Северной Европы"
            ]
        },
        "iitto_institute": {
            "name": "Институт информационных технологий и технологического образования",
            "departments": [
                "1. Кафедра информационных систем",
                "2. Кафедра информационных технологий и электронного обучения",
                "3. Кафедра технологического образования",
                "4. Кафедра цифрового образования"
            ]
        },
        "history_institute": {
            "name": "История и социальные науки",
            "departments": [
                "1. Кафедра всеобщей истории",
                "2. Кафедра истории",
                "3. Кафедра истории России с древнейших времен до начала XIX века",
                "4. Кафедра истории религий и теологии",
                "5. Кафедра методики обучения истории и обществознанию",
                "6. Кафедра политологии",
                "7. Кафедра русской истории (XIX-XXI вв.)",
                "8. Кафедра социологии"
            ]
        },
        "music_institute": {
            "name": "Музыка, театр и хореография",
            "departments": [
                "1. Кафедра музыкально-инструментальной подготовки",
                "2. Кафедра музыкального воспитания и образования",
                "3. Кафедра сольного пения",
                "4. Кафедра театрального искусства",
                "5. Кафедра хореографического искусства",
                "6. Кафедра хорового дирижирования"
            ]
        },
        "north_institute": {
            "name": "Народы Севера",
            "departments": [
                "1. Кафедра алтайских языков, фольклора и литературы",
                "2. Кафедра палеоазиатских языков, фольклора и литературы",
                "3. Кафедра уральских языков, фольклора и литературы",
                "4. Кафедра этнокультурологии"
            ]
        },
        "teach_institute": {
            "name": "Педагогика",
            "departments": [
                "1. Кафедра истории педагогики и образования",
                "2. Кафедра педагогики школы",
                "3. Кафедра теории и методики непрерывного педагогического образования",
                "4. Кафедра теории и методики воспитания и социальной работы"
            ]
        },
        "psycho_institute": {
            "name": "Психология",
            "departments": [
                "1. Кафедра клинической психологии и психологической помощи",
                "2. Кафедра общей и социальной психологии",
                "3. Кафедра психологии профессиональной деятельности и информационных технологий в образовании",
                "4. Кафедра психологии развития и образования"
            ]
        },
        "Russia_institute": {
            "name": "Русский язык как иностранный",
            "departments": [
                "1. Кафедра интенсивного обучения русскому языку как иностранному",
                "2. Кафедра русского языка как иностранного и методики его преподавания"
            ]
        },
        "pthysics_institute": {
            "name": "Физика",
            "departments": [
                "1. Кафедра методики обучения физике",
                "2. Кафедра общей и экспериментальной физики",
                "3. Кафедра теоретической физики и астрономии",
                "4. Кафедра физической электроники"
            ]
        },
        "sport_institute": {
            "name": "Физическая культура и спорт",
            "departments": [
                "1. Кафедра гимнастики и фитнес-технологий",
                "2. Кафедра методики обучения физкультуре и спортивной подготовки",
                "3. Кафедра оздоровительной физкультуры и адаптивного спорта",
                "4. Кафедра теории и организации физической культуры",
                "5. Кафедра физического воспитания и спортивно-массовой работы"
            ]
        },
        "fpeople_institute": {
            "name": "Философия человека",
            "departments": [
                "1. Кафедра связей с общественностью и рекламы",
                "2. Кафедра теории и истории культуры",
                "3. Кафедра философии",
                "4. Кафедра философской антропологии и истории философии",
                "5. Кафедра эстетики и этики"
            ]
        },
        "hudo_institute": {
            "name": "Художественное образование",
            "departments": [
                "1. Кафедра графики и скульптуры",
                "2. Кафедра декоративного искусства и дизайна",
                "3. Кафедра живописи",
                "4. Кафедра искусствоведения и педагогики искусства"
            ]
        },
        "economy_institute": {
            "name": "Экономика и управление",
            "departments": [
                "1. Кафедра государственного, муниципального и социального управления",
                "2. Кафедра отраслевой экономики и финансов",
                "3. Кафедра туризма, сервиса и гостеприимства",
                "4. Кафедра управления образованием и кадрового менеджмента",
                "5. Кафедра экономической теории и экономического образования"
            ]
        }
    }

    institute_data = institute_descriptions.get(institute_code)
    if institute_data:
        departments_text = "\n".join(institute_data["departments"])
        message = (
            f"Институт: {institute_data['name']}\n\n"
            f"Доступные кафедры:\n{departments_text}\n\n"
        )

        context.bot.send_message(
            chat_id=query.message.chat_id,
            text=message,
            reply_markup=keyboards.create_back_menu_keyboard()
        )

    if institute_code == "east_institute":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру института Востоковедение:",
            reply_markup=keyboards.east_institute_keyboard_inline()
        )
    elif institute_code == "childhood_institute":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру института Детство:",
            reply_markup=keyboards.childhood_institute_keyboard_inline()
        )
    elif institute_code == "idor_institute":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру института Институт дефектологического образования и реабилитации:",
            reply_markup=keyboards.idor_institute_keyboard_inline()
        )
    elif institute_code == "lang_institute":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру института Иностранные языки:",
            reply_markup=keyboards.lang_institute_keyboard_inline()
        )
    elif institute_code == "iitto_institute":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру института Институт информационных технологий и технологического образования:",
            reply_markup=keyboards.iitto_institute_keyboard_inline()
        )
    elif institute_code == "history_institute":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру института История и социальные науки:",
            reply_markup=keyboards.history_institute_keyboard_inline()
        )
    elif institute_code == "music_institute":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру института Музыка, театр и хореография:",
            reply_markup=keyboards.music_institute_keyboard_inline()
        )
    elif institute_code == "north_institute":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру института Народы Севера:",
            reply_markup=keyboards.north_institute_keyboard_inline()
        )
    elif institute_code == "teach_institute":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру института Педагогика:",
            reply_markup=keyboards.teach_institute_keyboard_inline()
        )
    elif institute_code == "psycho_institute":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру института Психология:",
            reply_markup=keyboards.psycho_institute_keyboard_inline()
        )
    elif institute_code == "Russia_institute":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру института Русский язык как иностранный:",
            reply_markup=keyboards.Russia_institute_keyboard_inline()
        )
    elif institute_code == "pthysics_institute":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру института Физика:",
            reply_markup=keyboards.pthysics_institute_keyboard_inline()
        )
    elif institute_code == "sport_institute":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру института Физическая культура и спорт:",
            reply_markup=keyboards.sport_institute_keyboard_inline()
        )
    elif institute_code == "fpeople_institute":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру института Философия человека:",
            reply_markup=keyboards.fpeople_institute_keyboard_inline()
        )
    elif institute_code == "hudo_institute":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру института Художественное образование:",
            reply_markup=keyboards.hudo_institute_keyboard_inline()
        )
    elif institute_code == "economy_institute":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите кафедру института Экономика и управление:",
            reply_markup=keyboards.economy_institute_keyboard_inline()
        )

    return DEPARTMENT


def handle_department_selection(update: Update, context: CallbackContext) -> None:
    """ Обработка выбора кафедры и поиск преподавателей """
    query = update.callback_query
    query.answer()

    department_mapping = {
        "zdorov_faculty": "здоровьесбережения и основ медицинских знаний",
        "medicine_faculty": "медико-валеологических дисциплин",
        "methodteachbzhd_faculty": "методики обучения безопасности жизнедеятельности",
        "basicsbzR_faculty": "основы безопасности и защиты Родины",
        "soshsafety_faculty": "социальной безопасности",
        "afchzh_faculty": "анатомии и физиологии человека и животных",
        "boteko_faculty": "ботаники и экологии",
        "zoogen_faculty": "зоологии и генетики",
        "methodobbioeko_faculty": "методики обучения биологии и экологии",
        "geogeo_faculty": "геологии и геоэкологии",
        "methodgeokr_faculty": "методики обучения географии и краеведению",
        "phizgeo_faculty": "физической географии и природопользования",
        "economygeo_faculty": "экономической географии",
        "algebra_faculty": "алгебры",
        "geometry_faculty": "геометрии",
        "mathanali_faculty": "математического анализа",
        "methodmathinfo_faculty": "методики обучения математике и информатике",
        "abroadbook_faculty": "зарубежной литературы",
        "mezhcult_faculty": "межкультурной коммуникации",
        "obrtechn_faculty": "образовательных технологий в филологии",
        "russianlang_faculty": "русского языка",
        "russianbook_faculty": "русской литературы",
        "neorg_faculty": "неорганической химии",
        "orgch_faculty": "органической химии",
        "chemistreko_faculty": "химического и экологического образования",
        "gos_faculty": "государственного права",
        "grazhd_faculty": "гражданского права",
        "mezhpravo_faculty": "международного права",
        "theorypravogr_faculty": "теории права и гражданско-правового образования",
        "criminal_faculty": "уголовного права",
        "criminalprocess_faculty": "уголовного процесса",
        "east1_institute": "восточных языков и лингводидактики",
        "east2_institute": "древневосточных языков",
        "east3_institute": "китайской филологии",
        "east4_institute": "языков и культур исламского мира",
        "childhood1_institute": "возрастной психологии и педагогики семьи",
        "childhood2_institute": "дошкольной педагогики",
        "childhood3_institute": "начального естественно-математического образования",
        "childhood4_institute": "педагогики начального образования и художественногого развития ребенка",
        "childhood5_institute": "раннего обучения иностранным языкам",
        "childhood6_institute": "языкового и литературного образования ребенка",
        "idor1_institute": "логопедии",
        "idor2_institute": "олигофренопедагогики",
        "idor3_institute": "основ дефектологии и реабилитологии",
        "idor4_institute": "сурдопедагогики",
        "idor5_institute": "тифлопедагогики",
        "lang1_institute": "английского языка для профессиональной коммуникации",
        "lang2_institute": "английского языка и лингвострановедения",
        "lang3_institute": "английской филологии",
        "lang4_institute": "интенсивного обучения иностранным языкам",
        "lang5_institute": "методики обучения иностранным языкам",
        "lang6_institute": "немецкого и романских языков для профессиональной коммуникации",
        "lang7_institute": "немецкой филологии",
        "lang8_institute": "перевода",
        "lang9_institute": "романской филологии",
        "lang10_institute": "языков Северной Европы",
        "iitto1_institute": "информационных систем",
        "iitto2_institute": "информационных технологий и электронного обучения",
        "iitto3_institute": "технологического образования",
        "iitto4_institute": "цифрового образования",
        "history1_institute": "всеобщей истории",
        "history2_institute": "истории",
        "history3_institute": "истории России с древнейших времен до начала XIX века",
        "history4_institute": "истории религий и теологии",
        "history5_institute": "методики обучения истории и обществознанию",
        "history6_institute": "политологии",
        "history7_institute": "русской истории (XIX-XXI вв.)",
        "history8_institute": "социологии",
        "music1_institute": "музыкально-инструментальной подготовки",
        "music2_institute": "музыкального воспитания и образования",
        "music3_institute": "сольного пения",
        "music4_institute": "театрального искусства",
        "music5_institute": "хореографического искусства",
        "music6_institute": "хорового дирижирования",
        "north1_institute": "алтайских языков, фольклора и литературы",
        "north2_institute": "палеоазиатских языков, фольклора и литературы",
        "north3_institute": "уральских языков, фольклора и литературы",
        "north4_institute": "этнокультурологии",
        "teach1_institute": "истории педагогики и образования",
        "teach2_institute": "педагогики школы",
        "teach3_institute": "теории и методики непрерывного педагогического образования",
        "teach4_institute": "теории и методики воспитания и социальной работы",
        "psycho1_institute": "клинической психологии и психологической помощи",
        "psycho2_institute": "общей и социальной психологии",
        "psycho3_institute": "психологии профессиональной деятельности и информационных технологий в образовании",
        "psycho4_institute": "психологии развития и образования",
        "Russia1_institute": "интенсивного обучения русскому языку как иностранному",
        "Russia2_institute": "русского языка как иностранного и методики его преподавания",
        "pthysics1_institute": "методики обучения физике",
        "pthysics2_institute": "общей и экспериментальной физики",
        "pthysics3_institute": "теоретической физики и астрономии",
        "pthysics4_institute": "физической электроники",
        "sport1_institute": "гимнастики и фитнес-технологий",
        "sport2_institute": "методики обучения физкультуре и спортивной подготовки",
        "sport3_institute": "оздоровительной физкультуры и адаптивного спорта",
        "sport4_institute": "теории и организации физической культуры",
        "sport5_institute": "физического воспитания и спортивно-массовой работы",
        "fpeople1_institute": "связей с общественностью и рекламы",
        "fpeople2_institute": "теории и истории культуры",
        "fpeople3_institute": "философии",
        "fpeople4_institute": "философской антропологии и истории философии",
        "fpeople5_institute": "эстетики и этики",
        "hudo1_institute": "графики и скульптуры",
        "hudo2_institute": "декоративного искусства и дизайна",
        "hudo3_institute": "живописи",
        "hudo4_institute": "искусствоведения и педагогики искусства",
        "economy1_institute": "государственного, муниципального и социального управления",
        "economy2_institute": "отраслевой экономики и финансов",
        "economy3_institute": "туризма, сервиса и гостеприимства",
        "economy4_institute": "управления образованием и кадрового менеджмента",
        "economy5_institute": "экономической теории и экономического образования",
        "not_specified": None
    }

    department_code = query.data
    search_term = department_mapping.get(department_code)

    if not search_term and department_code != "not_specified":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Ошибка: кафедра не распознана",
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return

    # Поиск преподавателей
    professors = []
    if 'current_professors' in context.user_data:
        source_list = context.user_data['current_professors']
        for prof in source_list:
            department_name = prof['department'].lower().strip()
            if department_code == "not_specified" and (not department_name or "не указано" in department_name):
                professors.append(prof)
            elif search_term and search_term.lower() in department_name:
                professors.append(prof)
    else:
        try:
            with open(CSV_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    department = row['department'].lower().strip()

                    # Для "не указано"
                    if department_code == "not_specified" and (not department or department == "не указано"):
                        professors.append(row)

                    # Для обычных кафедр
                    elif search_term and search_term.lower() in department:
                        professors.append(row)

        except Exception as e:
            context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"Ошибка при поиске: {str(e)}",
                reply_markup=keyboards.create_back_menu_keyboard()
            )
            return

    if not professors:
        message = (
            f"Преподаватели не найдены."
            if department_code == "not_specified"
            else f"На кафедре '{search_term}' преподаватели не найдены."
        )
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text=message,
            reply_markup=keyboards.create_back_menu_keyboard()
        )
    else:
        context.user_data.update({
            'current_professors': professors,
            'current_department': ("Не указано" if department_code == "not_specified" else search_term)
        })

        # Создание пронумерованный список преподавателей
        professors_list = ""
        for i, prof in enumerate(professors, 1):
            professors_list += f"{i}. {prof['name']}\n"

        # Создание инлайн-клавиатуру с номерами преподавателей
        professor_names = [prof['name'] for prof in professors]
        inline_keyboard = keyboards.create_numbered_keyboard(professor_names, "prof_")

        context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"Кафедра: {context.user_data['current_department']}\n"
                 f"Найдено преподавателей: {len(professors)}\n\n"
                 f"Список преподавателей:\n{professors_list}\n"
                 "Выберите номер преподавателя:",
            reply_markup=inline_keyboard
        )

        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Или используйте кнопки для действий со всеми результатами:",
            reply_markup=keyboards.department_menu_keyboard()
        )


def handle_department_action(update: Update, context: CallbackContext) -> int:
    """ Обработка действий после выбора кафедры """
    text = update.message.text
    logger.info(f"handle_department_action вызвана с текстом: {text}")

    if text == "Вывод по всем":
        show_all_department_professors(update, context)
        return DEPARTMENT

    elif text == "Следующий фильтр":
        show_next_filter_options(update, context)
        return DEPARTMENT

    elif text == "Назад":
        update.message.reply_text(
            "Возврат к выбору кафедры:",
            reply_markup=keyboards.department_keyboard()
        )
        return DEPARTMENT

    elif text == "Главное меню":
        show_menu(update, context)
        return ConversationHandler.END
    else:
        update.message.reply_text(
            "Пожалуйста, выберите вариант из меню.",
            reply_markup=keyboards.department_menu_keyboard()
        )
        return DEPARTMENT


def show_all_department_professors(update: Update, context: CallbackContext) -> None:
    """ Показать информацию о всех преподавателях кафедры """
    if 'current_professors' not in context.user_data:
        update.message.reply_text(
            "Данные не найдены. Пожалуйста, выполните поиск заново.",
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return

    professors = context.user_data['current_professors']
    department = context.user_data.get('current_department', 'Неизвестная кафедра')

    update.message.reply_text(
        f"Все преподаватели кафедры '{department}':",
        reply_markup=keyboards.create_back_menu_keyboard()
    )

    for prof in professors:
        update.message.reply_text(
            MSG_TEMPLATE.format(
                name=prof['name'],
                degree=prof['degree'],
                phone=prof['phone'],
                email=prof['email'],
                department=prof.get('department', department),
                url=prof['url']
            ),
            parse_mode='HTML',
            disable_web_page_preview=True
        )


def show_next_filter_options(update: Update, context: CallbackContext) -> None:
    """ Показать options для следующего фильтра """
    if 'current_professors' not in context.user_data:
        update.message.reply_text(
            "Данные не найдены. Пожалуйста, выполните поиск заново.",
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return

    professors = context.user_data['current_professors']
    department = context.user_data.get('current_department', 'Неизвестная кафедра')

    update.message.reply_text(
        f"Кафедра: {department}\n"
        f"Найдено преподавателей: {len(professors)}\n\n"
        "Выберите следующий критерий фильтрации:",
        reply_markup=keyboards.choiceafterdepartment_keyboard()
    )


def handle_professor_selection(update: Update, context: CallbackContext) -> None:
    """ Обработка выбора конкретного преподавателя из списка """
    query = update.callback_query
    query.answer()

    if 'current_professors' not in context.user_data:
        query.edit_message_text(
            "Данные не найдены. Пожалуйста, выполните поиск заново.",
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return

    professor_index = int(query.data.split('_')[1]) - 1
    professors = context.user_data['current_professors']

    if professor_index < 0 or professor_index >= len(professors):
        query.edit_message_text(
            "Преподаватель не найден.",
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return

    prof = professors[professor_index]
    department = context.user_data.get('current_department', 'Неизвестная кафедра')

    query.edit_message_text(
        MSG_TEMPLATE.format(
            name=prof['name'],
            degree=prof['degree'],
            phone=prof['phone'],
            email=prof['email'],
            department=prof.get('department', department),
            url=prof['url']
        ),
        parse_mode='HTML',
        disable_web_page_preview=True
    )

    context.bot.send_message(
        chat_id=query.message.chat_id,
        text="Выберите следующее действие:",
        reply_markup=keyboards.create_back_menu_keyboard()
    )


def choicedegree(update: Update, context: CallbackContext) -> int:
    """ Выбор кнопки 'По ученой степени' """
    if update.callback_query:
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat_id
        context.bot.send_message(
            chat_id=chat_id,
            text="Выберите ученую степень:",
            reply_markup=keyboards.degree_keyboard_inline()
        )
        context.bot.send_message(
            chat_id=chat_id,
            text="Или выберите другое действие:",
            reply_markup=keyboards.degree_keyboard()
        )
    else:
        update.message.reply_text(
            "Выберите ученую степень:",
            reply_markup=keyboards.degree_keyboard_inline()
        )
        update.message.reply_text(
            "Или выберите другое действие:",
            reply_markup=keyboards.degree_keyboard()
        )

    context.user_data['waiting_for_degree'] = True
    return DEGREE


def handle_degree_selection(update: Update, context: CallbackContext) -> None:
    """ Обработка выбора ученой степени """
    query = update.callback_query
    query.answer()

    degree_mapping = {
        "candidat": "кандидат",
        "doctor": "доктор"
    }

    degree_code = query.data
    degree_name = degree_mapping.get(degree_code)

    if not degree_name:
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Ошибка: ученая степень не распознана",
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return

    professors = []

    if 'current_professors' in context.user_data and context.user_data['current_professors']:
        source_list = context.user_data['current_professors']
        for prof in source_list:
            if degree_name.lower() in prof['degree'].lower():
                professors.append(prof)
    else:
        try:
            with open(CSV_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if degree_name.lower() in row['degree'].lower():
                        professors.append(row)
        except Exception as e:
            context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"Ошибка при поиске: {str(e)}",
                reply_markup=keyboards.create_back_menu_keyboard()
            )
            return

    context.user_data.update({
        'current_professors': professors,
        'current_degree': degree_name
    })

    if not professors:
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"Преподавателей с ученой степенью '{degree_name}' не найдено",
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return

    # Определение, какое меню показывать
    is_initial_search = 'current_professors' not in context.user_data or not context.user_data.get('is_filtered_search', False)

    if is_initial_search:
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"Найдено преподавателей с ученой степенью '{degree_name}': {len(professors)}. "
            "Выберите дальнейшие действие для отбора:",
            reply_markup=keyboards.choiceafterdegree_keyboard()
        )
        context.user_data['is_filtered_search'] = False # флаг, что это был не фильтрованный поиск
    else:
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"Найдено преподавателей с ученой степенью '{degree_name}': {len(professors)}. "
            "Вы можете вывести информацию по найденным преподавателям. Или вернуться назад, или сразу в главное меню.",
            reply_markup=keyboards.choiceafterdegreefromthelist_keyboard()
        )
        context.user_data['is_filtered_search'] = True # флаг, что это был фильтрованный поиск


def handle_degree_not_found(update: Update, context: CallbackContext) -> None:
    """ Обработка кнопки 'Не указано' для ученой степени """
    professors = []

    if 'current_professors' in context.user_data and context.user_data['current_professors']:
        source_list = context.user_data['current_professors']
        for prof in source_list:
            if not prof['degree'].strip() or "ученой степени не имеет" in prof['degree'].lower():
                professors.append(prof)

    else:
        try:
            with open(CSV_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if not row['degree'].strip() or "ученой степени не имеет" in row['degree'].lower():
                        professors.append(row)
        except Exception as e:
            update.message.reply_text(
                f"Ошибка при поиске: {str(e)}",
                reply_markup=keyboards.create_back_menu_keyboard()
            )
            return

        context.user_data.update({
            'current_professors': professors,
            'current_degree': "ученой степени не имеет"
        })

        if not professors:
            update.message.reply_text(
                "Преподавателей без указанной ученой степени не найдено",
                reply_markup=keyboards.create_back_menu_keyboard()
            )
            return

        # Определение, какое меню показывать
        is_initial_search = 'is_filtered_search' not in context.user_data or not context.user_data.get(
            'is_filtered_search', False)

        if is_initial_search:
            update.message.reply_text(
                f"Найдено преподавателей без указанной ученой степени: {len(professors)}. "
                "Выберите дальнейшие действие для отбора:",
                reply_markup=keyboards.choiceafterdegree_keyboard()
            )
            context.user_data['is_filtered_search'] = False
        else:
            update.message.reply_text(
                f"Найдено преподавателей без указанной ученой степени: {len(professors)}. "
                "Вы можете вывести информацию по найденным преподавателям. Или вернуться назад, или сразу в главное меню.",
                reply_markup=keyboards.choiceafterdegreefromthelist_keyboard()
            )
            context.user_data['is_filtered_search'] = True


def handle_degree_action(update: Update, context: CallbackContext) -> None:
    """ Обработка действий после выбора ученой степени """
    text = update.message.text
    logger.info(f"handle_degree_action вызвана с текстом: {text}")

    if text == "Вывод по всем":
        show_all_degree_professors(update, context)
        return DEGREE

    elif text == "По фамилии":
        update.message.reply_text(
            "Введите фамилию для поиска:",
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        context.user_data['next_filter'] = 'surname'
        return DEGREE

    elif text == "По кафедре":
        update.message.reply_text(
            "Выберите тип подразделения:",
            reply_markup=keyboards.department_keyboard()
        )
        context.user_data['next_filter'] = 'department'
        return DEGREE

    elif text == "Назад":
        update.message.reply_text(
            "Возврат к выбору ученой степени:",
            reply_markup=keyboards.degree_keyboard()
        )
        return DEGREE

    elif text == "Главное меню":
        show_menu(update, context)
        return ConversationHandler.END
    else:
        update.message.reply_text(
            "Пожалуйста, выберите вариант из меню.",
            reply_markup=keyboards.degree_keyboard_inline()
        )
        return DEGREE



def show_all_degree_professors(update: Update, context: CallbackContext) -> None:
    """ Показать всех преподавателей с выбранной ученой степенью """
    if 'current_professors' not in context.user_data:
        update.message.reply_text(
            "Данные не найдены. Пожалуйста, выполните поиск заново.",
            reply_markup=keyboards.create_back_menu_keyboard()
        )
        return

    professors = context.user_data['current_professors']
    degree = context.user_data.get('current_degree', 'Неизвестная степень')

    update.message.reply_text(
        f"Все преподаватели с ученой степенью '{degree}':",
        reply_markup=keyboards.choiceafterdegree_keyboard()
    )

    for prof in professors:
        update.message.reply_text(
            MSG_TEMPLATE.format(
                name=prof['name'],
                degree=prof['degree'],
                phone=prof['phone'],
                email=prof['email'],
                department=prof['department'],
                url=prof['url']
            ),
            parse_mode='HTML',
            disable_web_page_preview=True
        )


def reset_search_context(context: CallbackContext) -> None:
    """ Сброс контекста поиска """
    keys_to_remove = ['current_professors', 'found_professors', 'current_department', 'current_degree', 'is_filtered_search']
    for key in keys_to_remove:
        if key in context.user_data:
            del context.user_data[key]


def handle_text_message(update: Update, context: CallbackContext) -> int:
    """ Обрабатывает все текстовые сообщения и определяет контекст """
    user_text = update.message.text.strip()

    # Обработка обычных кнопок ReplyKeyboard
    if user_text == keyboards.SURNAME_BUTTON:
        return choicesurname(update, context)

    # Проверка состояния ожидания ввода ФИО
    elif context.user_data.get('waiting_for_fullname'):
        context.user_data['waiting_for_fullname'] = False
        return process_fullname_input(update, context)

    # Проверка состояния ожидания ввода фамилии
    elif context.user_data.get('waiting_for_surname'):
        context.user_data['waiting_for_surname'] = False
        return process_surname_input(update, context)

    # Если не в состоянии ожидания, показ меню
    else:
        update.message.reply_text(
            text="Пожалуйста, выберите вариант из меню.",
            reply_markup=keyboards.start_keyboard()
        )
        return ConversationHandler.END
