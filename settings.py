import os
from dotenv import load_dotenv

load_dotenv()

user_email = os.getenv('user_email')
user_pass = os.getenv('user_pass')