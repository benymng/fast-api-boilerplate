"""
Optional scheduler for background tasks
Run this as a separate service if you need scheduled jobs
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', minutes=5)
def example_job():
    """Example scheduled job that runs every 5 minutes"""
    logger.info(f"Example job executed at {datetime.now()}")
    # Add your scheduled task logic here


@scheduler.scheduled_job('cron', hour=0, minute=0)
def daily_job():
    """Example job that runs daily at midnight"""
    logger.info(f"Daily job executed at {datetime.now()}")
    # Add your daily task logic here


if __name__ == "__main__":
    logger.info("Starting scheduler...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped")
