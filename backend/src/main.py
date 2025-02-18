from typing import Annotated
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, Request
from src.users.models import UserInDB
from src.auth.utils import get_current_user
from src.auth.router import router as auth_router
from src.users.router import router as users_router
from src.specialization.router import router as specialization_router
from src.department.router import router as departments_router

# from azure.monitor.opentelemetry import configure_azure_monitor
from logging import Logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        import logging

        # Configure OpenTelemetry to use Azure Monitor with the
        # APPLICATIONINSIGHTS_CONNECTION_STRING environment variable.
        logger = logging.getLogger("custom_logger")  # Create a custom logger
        logger.setLevel(logging.DEBUG)
        raise NotImplementedError("Azure Monitor is not yet supported")
        # configure_azure_monitor(
        #     connection_string="<your-connection-string>",
        # )
    except Exception as e:
        import logging

        # Set up the logger
        logger.setLevel(logging.DEBUG)

        # Create console handler and set its log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Create a formatter and set it for the console handler
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

        # Add the console handler to the logger
        if (
            not logger.hasHandlers()
        ):  # Avoid adding multiple handlers in case this is run multiple times
            logger.addHandler(console_handler)

        # Disable all other loggers except your custom one
        logging.getLogger().setLevel(
            logging.DEBUG
        )  # This disables logs from other libraries

        # Example log message
        logger.debug("Logging setup complete and ready for debugging")
        logger.warning(f"Failed to configure Azure Monitor: {e}")
    app.state.logger = logger
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(specialization_router)
app.include_router(departments_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def read_root(request: Request):
    logger: Logger = request.app.state.logger
    logger.debug("Hello, World!")
    return {"Hello": "World"}


@app.get("/health")
async def protected_api(user: Annotated[UserInDB, Depends(get_current_user)]):
    print(user)
    return {"message": "Hello, World!"}
