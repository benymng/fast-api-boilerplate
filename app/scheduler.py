import logging
from datetime import UTC, datetime

from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BlockingScheduler(timezone="UTC")


@scheduler.scheduled_job("interval", minutes=5)
def example_job() -> None:
    logger.info("Example scheduled job ran at %s", datetime.now(UTC))


@scheduler.scheduled_job("cron", hour=0, minute=0)
def daily_job() -> None:
    logger.info("Daily scheduled job ran at %s", datetime.now(UTC))


def main() -> None:
    logger.info("Starting scheduler")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped")


if __name__ == "__main__":
    main()
