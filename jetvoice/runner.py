# runner.py

import os
from loguru import logger
from watchfiles import run_process

from jetvoice.main import main as jetvoice_main

def main():
    """
    Development runner that starts the main application with auto-reloading.
    """
    # The directory to watch for changes.
    watch_dir = './jetvoice'
    
    logger.info(f"Starting runner. Watching for changes in '{os.path.abspath(watch_dir)}'...")
    
    # run_process will start the 'jetvoice_main' function in a separate process.
    # Whenever a file changes in 'watch_dir', it will terminate the process
    # and start a new one.
    run_process(watch_dir, target=jetvoice_main)

if __name__ == "__main__":
    main()