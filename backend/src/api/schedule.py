import logging

from fastapi import APIRouter
from fastapi_utils.tasks import repeat_every


from ..dinnerme.settings import Schedule as ScheduleSettings
from .shared import manager


logger = logging.getLogger()
router = APIRouter()


@router.on_event("startup")
@repeat_every(seconds=ScheduleSettings.fetch, raise_exceptions=True)  # 4 minutes
async def collect_data() -> None:
    try:
        logger.info("collect_data: Collecting data...")
        await manager.run(n_weeks=ScheduleSettings.n_weeks)
    except:
        logger.error("collect_data: Failed to collect data", exc_info=True)
    else:
        logger.info("collect_data: Finished collecting data...")
