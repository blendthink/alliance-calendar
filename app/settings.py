import os
from os.path import join, dirname

from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

WORKPLACE_URL = os.environ.get("WORKPLACE_URL")
GOOGLE_EMAIL_ADDRESS = os.environ.get("GOOGLE_EMAIL_ADDRESS")
