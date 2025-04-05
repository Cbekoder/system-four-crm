import os
from pathlib import Path
import subprocess
from datetime import datetime
import requests
import environ
import shutil

BASE_DIR = Path(__file__).resolve().parent

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

USE_POSTGRES = env.bool('USE_POSTGRES', False)
DB_NAME = env.str('DB_NAME')
DB_USER = env.str('DB_USER')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_HOST = env.str('DB_HOST', 'localhost')
DB_PORT = env.str('DB_PORT', '5432')
TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')
BACKUP_CHANNEL_ID = env.str('BACKUP_CHANNEL_ID')
BACKUP_DIR = "backups"

# Ensure backup directory exists
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(BACKUP_DIR, f"{DB_NAME}_backup_{timestamp}.{'sql' if USE_POSTGRES else 'sqlite3'}")

def backup_postgres():
    try:
        cmd = [
            "pg_dump",
            "-U", DB_USER,
            "-h", DB_HOST,
            "-p", DB_PORT,
            "-f", backup_file,
            DB_NAME
        ]
        env = os.environ.copy()
        env["PGPASSWORD"] = DB_PASSWORD

        result = subprocess.run(cmd, env=env, check=True, capture_output=True, text=True)
        print(f"PostgreSQL backup created: {backup_file}")
        return backup_file
    except subprocess.CalledProcessError as e:
        print(f"Error during PostgreSQL backup: {e.stderr}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def backup_sqlite():
    try:
        if not os.path.exists("db.sqlite3"):
            raise FileNotFoundError(f"SQLite database file {'db.sqlite3'} not found!")
        shutil.copyfile("db.sqlite3", backup_file)
        print(f"SQLite backup created: {backup_file}")
        return backup_file
    except Exception as e:
        print(f"Error during SQLite backup: {e}")
        return None


# Function to send the backup to Telegram
def send_to_telegram(backup_path):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        with open(backup_path, "rb") as f:
            files = {"document": (os.path.basename(backup_path), f)}
            data = {"chat_id": BACKUP_CHANNEL_ID, "caption": f"Database backup: {os.path.basename(backup_path)}"}
            response = requests.post(url, files=files, data=data)

        if response.status_code == 200:
            print(f"Backup sent to Telegram channel: {backup_path}")
        else:
            print(f"Failed to send to Telegram: {response.text}")
    except Exception as e:
        print(f"Error sending to Telegram: {e}")


if __name__ == "__main__":
    if USE_POSTGRES:
        backup_path = backup_postgres()
    else:
        backup_path = backup_sqlite()

    if backup_path and os.path.exists(backup_path):
        send_to_telegram(backup_path)
    else:
        print("Backup failed, nothing sent to Telegram.")