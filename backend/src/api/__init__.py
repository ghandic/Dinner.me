from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .mongo_utils import close_mongo_connection, connect_to_mongo
from .router import router
from .schedule import router as scheduling_router
from ..dinnerme.settings import General as GeneralSettings

api = FastAPI()
api.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"],
)
api.add_event_handler("startup", connect_to_mongo)
api.add_event_handler("shutdown", close_mongo_connection)

responses = {
    200: {"description": "Request was successful."},
    400: {"description": "Request was unsuccessful. Client error has occurred."},
    500: {"description": "Request was unsuccessful. Server error has occurred. "},
}

api.include_router(router, prefix="/dinner", responses=responses)
if GeneralSettings.collecting:
    api.include_router(scheduling_router, prefix="/tmp", tags=["tmp"], responses=responses)
