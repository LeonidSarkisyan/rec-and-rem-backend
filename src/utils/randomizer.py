import string
import random


def get_random_string(length: int = 40):
    randon_string = ''
    for i in range(length):
        r = random.choice(string.ascii_letters)
        randon_string += r

    return randon_string
