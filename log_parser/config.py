"""Config variables module."""
import os

LOGS_DIR = os.getenv('LOGS_DIR', 'logs')
MAX_BYTES = int(os.getenv('MAX_BYTES', 10**6))
BACKUP_COUNT = int(os.getenv('BACKUP_COUNT', 5))
