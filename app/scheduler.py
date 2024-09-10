from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app import logger
from app.toll_fee_calculator.calculator import run_toll_fee_calculations


class Scheduler(AsyncIOScheduler):
    """Scheduler for tasks."""

    def __init__(self, timezone="Europe/Stockholm") -> None:
        super().__init__(timezone=timezone)

    def add_calculator_task(self, hour_to_run_at: int = 23) -> None:
        """This is a simplified version of how the scheduling should be done.
        In practice, we should be passing the date as an argument in case the
        running of the run_toll_fee_calculations would be delayed or run at
        another time."""

        self.add_job(
            run_toll_fee_calculations,
            trigger="cron",
            hour=hour_to_run_at,
            name="run_toll_fee_calculations",
        )
        logger.info("Task added: run_toll_fee_calculations")


scheduler = Scheduler()
