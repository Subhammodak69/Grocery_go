from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

_scheduler = None  # prevent duplicate scheduler on hot reload

def sync_databases():
    logger.info("🔄 Syncing cloud → local...")
    try:
        call_command('sync_all')
        logger.info("✅ Sync complete")
    except Exception as e:
        logger.error(f"❌ Sync failed: {e}")

def push_databases():
    logger.info("🚀 Pushing local → cloud...")
    try:
        call_command('push_to_cloud')
        logger.info("✅ Push complete")
    except Exception as e:
        logger.error(f"❌ Push failed: {e}")

def start():
    global _scheduler

    # Prevent duplicate schedulers (Django reloader runs ready() twice)
    if _scheduler and _scheduler.running:
        logger.info("⏭️ Scheduler already running, skipping")
        return

    _scheduler = BackgroundScheduler()

    _scheduler.add_job(
        sync_databases,
        trigger=IntervalTrigger(hours=12),
        id='sync_cloud_to_local',
        name='Sync Cloud → Local',
        replace_existing=True,
    )

    _scheduler.add_job(
        push_databases,
        trigger=IntervalTrigger(hours=12, start_date='2024-01-01 00:01:00'),
        id='push_local_to_cloud',
        name='Push Local → Cloud',
        replace_existing=True,
    )

    _scheduler.start()
    logger.info("📅 Scheduler started — runs every 12 hours")