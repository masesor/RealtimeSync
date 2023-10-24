import time
import os
import yaml
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class BackupHandler(FileSystemEventHandler):
    def __init__(self, src_path, dest_path):
        self.src_path = src_path
        self.dest_path = dest_path

    def on_modified(self, event):
        self.backup()

    def on_created(self, event):
        self.backup()

    def on_moved(self, event):
        self.backup()

    def backup(self):
        if os.path.isdir(self.src_path):
            src = f"{self.src_path}/"
            dest = self.dest_path
        else:
            src = self.src_path
            dest = os.path.dirname(self.dest_path)
        
        logging.info(f"Starting backup: {src} to {dest}")
        
        result = subprocess.run(['rsync', '-avh', '--checksum', '--delete', src, dest], capture_output=True, text=True)
        
        if result.returncode == 0:
            logging.info(f"Backup completed: {src} to {dest}")
        else:
            logging.error(f"Backup failed for: {src} to {dest}. Error: {result.stderr}")

def load_config(yaml_file):
    with open(yaml_file, 'r') as f:
        config = yaml.safe_load(f)
    return config

def main():
    CONFIG_FILE = "./config.yaml"
    config = load_config(CONFIG_FILE)

    # Set up logging
    logging.basicConfig(filename=f'{config.log_location}/backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    directories = config.get('directories', [])
    TARGET_DIR = config.get('target_dir')

    for directory in directories:
        backup_dir = os.path.join(TARGET_DIR, os.path.basename(directory))
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Perform the initial sync
        handler = BackupHandler(directory, backup_dir)
        handler.backup()

        # Now set up the watchdog to monitor for changes
        event_handler = BackupHandler(directory, backup_dir)
        observer = Observer()
        observer.schedule(event_handler, directory, recursive=True)
        observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Backup script stopped.")

    observer.join()

if __name__ == "__main__":
    logging.info("Backup script started.")
    main()

