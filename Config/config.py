ADMIN_ID = 
LIST_ADMINS = []
API_ID =  # Админский

BOT_TOKEN = 

ARCHIVE = 
BOTID = 
BOTUSERNAME = '@pinanybot'

LINKTOBOT = 'https://t.me/pinanybot?start=invitelink'

LINKTOBOTFORWORKER = 'https://t.me/pinanybot?start=worker'

SUPPORTBOT = 'https://t.me/L_P_M_Support_Bot'

LOGNAME = "Logs/PINbot.log"
# LOGSTATE = 'INFO'
LOGSTATE = 'WARNING'

# Юзербот для слежения за постами
USERBOTID = 
USERBOTAPI = 
USERBOTAPIHASH = 
USERBOTPHONE = 
USERBOTUSERNAME = 
USERBOTSESSIONNAME = 
USERBOTSESSIONNAMECOPY = 

# Список статусов юзера
LISTOFUSERSTATUS = ['trial', 'vip', 'lead_1', 'lead_1_full', 'lead_2', 'employee']
LISTOFUSERPAY = ['trial', 'month_1', 'month_3', 'month_6', 'month_12']

# DataBase Local
NAME_FOR_BASE = 'PINbot'
DB_HOST = '127.0.0.1'
DB_USER = 'postgres'
DB_PASSWORD = 
DB_DATABASE = 'PINbot'
DB_TABLE = 'datausers'  # Основная таблица
DB_TABLE_REFS = 'refs'  # Таблица учёта рефералок

# Экспорт из базы в csv Админ
CSV_FILE = 'PINbot_'
LIST_SUBJECTS = ["id", "user_id", "username", "first_name", "last_name", "which_bot", "date_of_start", "date_of_use", "email", "come_from", "channel_title", "p", "t", "b", "button_text", "button_link", "post_id_archive", "channel_last_post", "bot_last_post", "user_bot_allowed", "user_channel_allowed", "user_bot_session", "is_payed", "date_of_pay", "date_of_end", "invited", "user_channel", "watch_on", "scheduler_on", "scheduler_time", "picture_id", "post_text"]

# Экспорт из базы в csv ВИП
CSV_FILE_2 = 'PINbot_Ref_'
LIST_SUBJECTS_REF_VIP = ["Юзернейм лида 1 уровня", "ID лида 1 уровня", "Дата оплаты", "Сумма оплаты", "Сумма по реф. программе", "Дата выплаты",
                     "Юзернейм лида 2 уровня", "ID лида 2 уровня", "Дата оплаты", "Сумма оплаты", "Сумма по реф. программе", "Дата выплаты"]
LIST_DATA_REF_VIP = "lead_1_username, lead_1, date_of_pay_lead_1, sum_of_pay_lead_1, sum_to_ref_0, date_payout_lead_1_to_0, " \
                "lead_2_username, lead_2, date_of_pay_lead_2, sum_of_pay_lead_2, sum_to_ref_lead_2_to_0, date_payout_lead_2_to_0"

# Экспорт из базы в csv Лид_1
LIST_SUBJECTS_REF = ["Юзернейм лида", "ID лида", "Дата оплаты", "Сумма оплаты", "Сумма по реф. программе", "Дата выплаты"]
LIST_DATA_REF = "lead_2_username, lead_2, date_of_pay_lead_2, sum_of_pay_lead_2, sum_to_ref_lead_2_to_1, date_payout_lead_2_to_1"

# Данные юмани
YOOCLIENTID = 
YOOREDIRECTURI = 
YOOWALLET = 
YOOTOKEN = 
