import os
import logging
from dotenv import load_dotenv
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler)
from commands import (start, show_menu, choicefullname, choicesurname, choicedepartment, choicedegree, process_fullname_input, process_surname_input, handle_department_type, handle_department_selection, handle_department_action, handle_degree_action, handle_degree_not_found, handle_institute_selection, handle_faculty_selection, handle_professor_selection, handle_text_message, handle_degree_selection)
import keyboards

from states import FULLNAME, SURNAME, DEPARTMENT, DEGREE

load_dotenv() # Загружаем переменные окружения из файла .env

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    except ImportError:
        pass

if not TOKEN:
    raise ValueError(
        "Токен бота не найден!"
    )

def main() -> None:
    """Основная функция для запуска бота."""

    # Создаем Updater и передаем ему токен бота
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Создаем ConversationHandler для управления состояниями
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('menu', show_menu),
            MessageHandler(Filters.regex(f'^{keyboards.BUTTON_MENU}$'), show_menu),
            MessageHandler(Filters.regex('^(По фамилии)$'), choicesurname),
            MessageHandler(Filters.regex('^(По кафедре)$'), choicedepartment),
            MessageHandler(Filters.regex('^(По ученой степени)$'), choicedegree),
            CallbackQueryHandler(choicedepartment, pattern='^department$'),
            CallbackQueryHandler(choicedegree, pattern='^degree$')
        ],
        states={
            FULLNAME: [
                MessageHandler(Filters.text & ~Filters.command, process_fullname_input)
            ],
            SURNAME: [
                MessageHandler(Filters.text & ~Filters.command, process_surname_input),
            ],
            DEPARTMENT: [
                MessageHandler(Filters.regex('^(Факультет|Институт|Не указано)$'), handle_department_type),
                MessageHandler(Filters.regex('^(Вывод по всем|Следующий фильтр|Назад|Главное меню)$'), handle_department_action),
            ],
            DEGREE: [
                MessageHandler(Filters.regex('^(Не указано)$'), handle_degree_not_found),
                MessageHandler(Filters.regex('^(Вывод по всем|По фамилии|По кафедре|Назад|Главное меню)$'), handle_degree_action)
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CommandHandler('menu', show_menu),
            MessageHandler(Filters.regex(f'^{keyboards.BUTTON_MENU}$'), show_menu),
            MessageHandler(Filters.regex(f'^{keyboards.BACK_BUTTON}$'), show_menu)
        ],
        allow_reentry=True,
    )

    dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text_message))

    # Обработчик для инлайн-кнопок
    dispatcher.add_handler(CallbackQueryHandler(choicefullname, pattern='^full_name$'))

    # Обработчик для выбора конкретного преподавателя
    dispatcher.add_handler(CallbackQueryHandler(handle_professor_selection, pattern='^prof_'))

    # Обработчик для факультетов/институтов
    dispatcher.add_handler(CallbackQueryHandler(handle_faculty_selection, pattern='^bzhd_faculty$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_faculty_selection, pattern='^b_faculty$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_faculty_selection, pattern='^g_faculty$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_faculty_selection, pattern='^math_faculty$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_faculty_selection, pattern='^filo_faculty$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_faculty_selection, pattern='^chemistry_faculty$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_faculty_selection, pattern='^ur_faculty$'))

    institute_patterns = [
        '^east_institute$', '^childhood_institute$', '^idor_institute$', '^lang_institute$',
        '^iitto_institute$', '^history_institute$', '^music_institute$',
        '^north_institute$', '^teach_institute$', '^psycho_institute$',
        '^Russia_institute$', '^pthysics_institute$', '^sport_institute$',
        '^fpeople_institute$', '^hudo_institute$', '^economy_institute$',
    ]
    for pattern in institute_patterns:
        dispatcher.add_handler(CallbackQueryHandler(handle_institute_selection, pattern=pattern))

    # Обработчик кафедр
    department_patterns = [
        '^zdorov_faculty$', '^medicine_faculty$', '^methodteachbzhd_faculty$', '^basicsbzR_faculty$', '^soshsafety_faculty$', '^afchzh_faculty$', '^boteko_faculty$', '^zoogen_faculty$', '^methodobbioeko_faculty$', '^geogeo_faculty$',
        '^methodgeokr_faculty$', '^phizgeo_faculty$', '^economygeo_faculty$', '^algebra_faculty$', '^geometry_faculty$', '^mathanali_faculty$', '^methodmathinfo_faculty$', '^abroadbook_faculty$', '^mezhcult_faculty$', '^obrtechn_faculty$',
        '^russianlang_faculty$', '^russianbook_faculty$', '^neorg_faculty$', '^orgch_faculty$', '^chemistreko_faculty$', '^gos_faculty$', '^grazhd_faculty$', '^mezhpravo_faculty$', '^theorypravogr_faculty$', '^criminal_faculty$',
        '^criminalprocess_faculty$', '^east1_institute$', '^east2_institute$', '^east3_institute$', '^east4_institute$', '^childhood1_institute$', '^childhood2_institute$', '^childhood3_institute$', '^childhood4_institute$', '^childhood5_institute$',
        '^childhood6_institute$', '^idor1_institute$', '^idor2_institute$', '^idor3_institute$', '^idor4_institute$', '^idor5_institute$', '^lang1_institute$', '^lang2_institute$', '^lang3_institute$', '^lang4_institute$',
        '^lang5_institute$', '^lang6_institute$', '^lang7_institute$', '^lang8_institute$', '^lang9_institute$', '^lang10_institute$', '^iitto1_institute$', '^iitto2_institute$', '^iitto3_institute$', '^iitto4_institute$',
        '^history1_institute$', '^history2_institute$', '^history3_institute$', '^history4_institute$', '^history5_institute$', '^history6_institute$', '^history7_institute$', '^history8_institute$', '^music1_institute$', '^music2_institute$',
        '^music3_institute$', '^music4_institute$', '^music5_institute$', '^music6_institute$', '^north1_institute$', '^north2_institute$', '^north3_institute$', '^north4_institute$', '^teach1_institute$', '^teach2_institute$',
        '^teach3_institute$', '^teach4_institute$', '^psycho1_institute$', '^psycho2_institute$', '^psycho3_institute$', '^psycho4_institute$', '^Russia1_institute$', '^Russia2_institute$', '^pthysics1_institute$', '^pthysics2_institute$',
        '^pthysics3_institute$', '^pthysics4_institute$', '^sport1_institute$', '^sport2_institute$', '^sport3_institute$', '^sport4_institute$', '^sport5_institute$', '^fpeople1_institute$', '^fpeople2_institute$', '^fpeople3_institute$',
        '^fpeople4_institute$', '^fpeople5_institute$', '^hudo1_institute$', '^hudo2_institute$', '^hudo3_institute$', '^hudo4_institute$', '^economy1_institute$', '^economy2_institute$', '^economy3_institute$', '^economy4_institute$', '^economy5_institute$', '^not_specified$'
    ]
    for pattern in department_patterns:
        dispatcher.add_handler(CallbackQueryHandler(handle_department_selection, pattern=pattern))

    # Обработчик ученой степени
    dispatcher.add_handler(CallbackQueryHandler(handle_degree_selection, pattern='^candidat$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_degree_selection, pattern='^doctor$'))

    # Запускаем бота
    updater.start_polling()
    logger.info("Бот запущен и начал опрос сервера Telegram...")


if __name__ == '__main__':
    main()