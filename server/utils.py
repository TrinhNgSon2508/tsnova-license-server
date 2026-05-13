import random
import string

def generate_license_key(plan="PRO"):
    chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

    return f"TSNOVA-{plan}-{chars[:4]}-{chars[4:8]}-{chars[8:12]}"