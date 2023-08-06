import random
import string

def generateKey(length, uppers=True, lowers=True, digits=True, punctuation=True, except_chars=""):
    pool = ""
    if (uppers):
        pool += string.ascii_uppercase
    if (lowers):
        pool += string.ascii_lowercase
    if (digits):
        pool += string.digits
    if (punctuation):
        pool += string.punctuation
    for c in except_chars:
        pool = pool.replace(c, "")
    return ''.join(random.SystemRandom().choice(pool) for _ in range(length))
