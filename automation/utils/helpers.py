import random
import string
from datetime import datetime, timedelta

def generate_random_email() -> str:
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test.user.{random_str}@workforce.test"

def generate_random_phone() -> str:
    return "9" + "".join(random.choices(string.digits, k=9))

def get_today_date_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")
