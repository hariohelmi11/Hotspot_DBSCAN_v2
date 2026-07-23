import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


def start_scheduler():
    scheduler.add_job(
        func=_daily_news_etl,
        trigger=CronTrigger(hour=2, minute=0),
        id="daily_news_etl",
        name="Daily News ETL",
        replace_existing=True,
    )
    scheduler.add_job(
        func=_weekly_dbscan,
        trigger=CronTrigger(day_of_week="sun", hour=3, minute=0),
        id="weekly_dbscan",
        name="Weekly DBSCAN",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("APScheduler started")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("APScheduler stopped")


def _daily_news_etl():
    from app.database import SessionLocal
    from app.services.etl.pipeline import run_etl_pipeline
    db = SessionLocal()
    try:
        result = run_etl_pipeline(db, source="news", year=2026)
        logger.info(f"Scheduled ETL completed: {result}")
    except Exception as e:
        logger.error(f"Scheduled ETL error: {e}")
    finally:
        db.close()


def _weekly_dbscan():
    from app.database import SessionLocal
    from app.services.dbscan_service import run_dbscan
    db = SessionLocal()
    try:
        result = run_dbscan(db)
        logger.info(f"Scheduled DBSCAN completed: {result}")
    except Exception as e:
        logger.error(f"Scheduled DBSCAN error: {e}")
    finally:
        db.close()
