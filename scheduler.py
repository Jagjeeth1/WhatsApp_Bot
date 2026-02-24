from apscheduler.schedulers.background import BackgroundScheduler
from linear_summary import send_pending_tasks


def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")


    scheduler.add_job(
        send_pending_tasks,
        trigger='cron',
        hour=8,
        minute=0
    )


    scheduler.add_job(
        send_pending_tasks,
        trigger='cron',
        hour=23,
        minute=0
    )

    scheduler.start()
    print("Scheduler started...")