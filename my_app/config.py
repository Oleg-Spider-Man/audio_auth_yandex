from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
SECRET_KEY = os.environ.get('SECRET_KEY')
YANDEX_CLIENT_ID = os.environ.get('YANDEX_CLIENT_ID')
YANDEX_REDIRECT_URI = os.environ.get('YANDEX_REDIRECT_URI')
SECRET_YANDEX = os.environ.get('SECRET_YANDEX')
