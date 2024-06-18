
import logging

logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)


ConsoleOutputHandler = logging.StreamHandler()

# Define a formatter that includes the class name in the log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(module)s.%(funcName)s)')

# Set the formatter for the console handler
ConsoleOutputHandler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(ConsoleOutputHandler)


