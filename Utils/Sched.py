import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from DB.DB_utils import update_values_db_two
from Utils.Autopost import first_post
sched = AsyncIOScheduler()


def run_scheduler(date_to_base, channel_id_here):
    try:
        sched.add_job(first_post, 'date', id=str(channel_id_here), run_date=date_to_base, args=(channel_id_here,))
        sched.start()
    except Exception as ex:
        logging.error(f"[Run scheduler] - {ex}", exc_info=True)


def stop_scheduler(user_id, user_channel):
    try:
        sched.remove_job(str(user_channel))
    except Exception as ex:
        logging.error(f"[Scheduler removing job] - {ex}", exc_info=True)

    # Проверить есть ли активные задания
    length_of_job_list = len(sched.get_jobs())
    if length_of_job_list == 0:
        try:
            sched.shutdown(wait=False)
        except Exception as ex:
            logging.error(f"[Scheduler_2 stop] - {ex}", exc_info=True)

    list_values_of_DB = f"scheduler_on='off'," \
                        f"scheduler_time=NULL"
    update_values_db_two(list_values_of_DB, 'user_id', user_id)


def stop_scheduler_2(user_id, user_channel):
    try:
        sched.remove_job(str(user_channel))
    except Exception as ex:
        logging.error(f"[Scheduler_2 removing job] - {ex}", exc_info=True)

    # Проверить есть ли активные задания
    length_of_job_list = len(sched.get_jobs())
    if length_of_job_list == 0:
        try:
            sched.shutdown(wait=False)
        except Exception as ex:
            logging.error(f"[Scheduler_2 stop] - {ex}", exc_info=True)

    list_values_of_DB = f"watch_on='off'," \
                        f"scheduler_on='off'," \
                        f"scheduler_time=NULL"
    update_values_db_two(list_values_of_DB, 'user_id', user_id)
