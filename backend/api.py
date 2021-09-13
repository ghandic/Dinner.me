import uvicorn
from src.api import api  # noqa
from src.dinnerme.logging_setup import setup_logging

setup_logging(path="/opt/working/logging.yaml")

# Initialize the FastAPI application
if __name__ == "__main__":
    uvicorn.run("api:api", port=8000, host="0.0.0.0", reload=True, log_config=None)
