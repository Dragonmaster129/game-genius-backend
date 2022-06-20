# Code copied from https://gist.github.com/markito/30a9bc2afbbfd684b31986c2de305d20
import uuid
import hashlib


def hashText(text, salt=None):
    """
        Basic hashing function for a text using random unique salt.
    """
    if salt is None:
        salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + text.encode()).hexdigest() + ':' + salt


def matchHashedText(hashedText, providedText):
    """
        Check for the text in the hashed text
    """
    _hashedText, salt = hashedText.split(':')
    return _hashedText == hashlib.sha256(salt.encode() + providedText.encode()).hexdigest()
