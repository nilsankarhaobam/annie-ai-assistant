import logging
import os

# Ensure logs folder exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# File path
LOG_FILE = os.path.join(LOG_DIR, "annie.log")

# Logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        # logging.StreamHandler()  # Console logs #comment out for hide the log detail in terminal chat
    ]
)

logger = logging.getLogger("AnnieLogger")
