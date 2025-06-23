import logging 
import sys
import os
from datetime import datetime

"""
A logger in Python refers to a part of the logging module, which is used to track events that happen when your code runs.

Instead of using print() for debugging or tracking what's going on, a logger:
- Saves logs to files
- Gives you timestamps, severity levels (INFO, DEBUG, WARNING, ERROR, CRITICAL)
- Lets you filter and control output
- Is production-level safe and clean
"""

# --------------------------------------------------------------
# STEP 1: Generate a unique log file name based on current date and time
# --------------------------------------------------------------
LOG_FILE = f"{datetime.now().strftime('%m-%d-%Y-%H-%M-%S')}.log"
"""
This creates a filename like '06-22-2025-19-30-45.log' using current date and time
So that each time the app runs, a new unique log file is generated.
"""

# --------------------------------------------------------------
# STEP 2: Create the 'logs' directory (if it doesn't exist) and set full log file path
# --------------------------------------------------------------
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
"""
This constructs a full path like 'C:/YourProject/logs/06-22-2025-19-30-45.log'
Where logs will be saved in a folder named 'logs'
"""

os.makedirs(logs_path, exist_ok=True)
"""
Creates the directory path if it doesn’t already exist.
The 'exist_ok=True' prevents an error if the folder is already there.
"""

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)
"""
This sets the final full path for the log file to be used by the logger.
"""

# --------------------------------------------------------------
# STEP 3: Set up basic logging configuration
# --------------------------------------------------------------
logging.basicConfig(
    filename=LOG_FILE_PATH,  # Set the destination log file path
    format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s',  # Log message format
    level=logging.INFO,  # Minimum level to log (INFO and above will be logged)
)

"""
Explanation of the logging format:
- %(asctime)s  → Timestamp of the log entry
- %(lineno)d   → Line number where the log was written
- %(name)s     → Name of the logger (often the module name)
- %(levelname)s → Level of the log (e.g., INFO, ERROR)
- %(message)s  → The actual log message
"""

# Example usage (you can add this at the bottom to test):
# logging.info("Logger is set up and ready to use.")
