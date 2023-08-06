import random
import string


def generate_api_key(length):
    s = ''
    while len(s) < length:
        s += ''.join(
            random.sample(
                string.digits + string.ascii_letters,
                62
            )
        )

    return s[:length]
