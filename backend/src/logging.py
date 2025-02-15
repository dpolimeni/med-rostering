import logging


# Set up the logger
logger = logging.getLogger("custom_logger")  # Create a custom logger
logger.setLevel(logging.DEBUG)

# Create console handler and set its log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the console handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Add the console handler to the logger
if (
    not logger.hasHandlers()
):  # Avoid adding multiple handlers in case this is run multiple times
    logger.addHandler(console_handler)

# Disable all other loggers except your custom one
logging.getLogger().setLevel(
    logging.CRITICAL
)  # This disables logs from other libraries

# Example log message
logger.debug("Logging setup complete and ready for debugging")
