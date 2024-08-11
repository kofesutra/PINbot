from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    # Основные
    on_start = State()
    select_getting_post = State()
    select_getting_post_0 = State()
    get_getting_post = State()
    receive_post = State()
    run_set_post = State()
    set_picture = State()
    get_picture = State()
    set_text = State()
    get_text = State()
    set_button = State()
    set_button_text = State()
    set_button_link = State()
    check = State()
    ok = State()
    corrections = State()
    publishing = State()
    get_date_time = State()
    confirm_date = State()
    # stop_start = State()
    stop = State()

    # Регистрация
    greeting = State()
    get_channel = State()
    confirm_channel = State()
    set_channel = State()
    check_admins = State()

    # Статус
    status = State()
    status_buttons = State()

    # Отложенный запуск
    get_year = State()
    get_month = State()
    get_day = State()
    get_hour = State()
    get_minutes = State()
    get_check = State()

    # Оплата
    payment = State()
    check_payment = State()

    # Работник
    employee = State()
    get_employee = State()
    check_employee = State()
    remove_employee = State()
    confirm_remove_employee = State()


class StatesAdmin(StatesGroup):
    admin = State()
    user_id_for_letter = State()
    letter_to_user = State()
    check_letter = State()

    run_message_mass = State()
    get_text_for_mass = State()
    check_letter_for_mass = State()
