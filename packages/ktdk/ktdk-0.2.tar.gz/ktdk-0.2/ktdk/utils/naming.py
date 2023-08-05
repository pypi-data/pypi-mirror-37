import re
import secrets
import string

from unidecode import unidecode

NOT_ALLOWED_FOR_NAME = string.punctuation.replace('_', '')


def slugify(text):
    """
    Simplifies ugly strings into something URL-friendly.
    >>> print slugify("[Some] _ Article's Title--")
    some-articles-title
    """

    # "[Some] _ Article's Title--"
    # "[some] _ article's title--"
    text = text.lower()

    # "[some] _ article's_title--"
    # "[some]___article's_title__"
    for c in [' ', '-', '.', '/']:
        text = text.replace(c, '_')

    # "[some]___article's_title__"
    # "some___articles_title__"
    text = re.sub('\W', '', text)
    # "some   articles title  "
    # "some articles title "
    text = re.sub('\s+', ' ', text)

    # "some articles title "
    # "some articles title"
    text = text.strip()

    # "some articles title"
    # "some-articles-title"
    text = text.replace(' ', '-')

    return text


def remove_punctuation(original: str) -> str:
    """Removes punctuation from string
    Args:
        original(str): Original string

    Returns(str): String with removed punctuation

    """
    table = original.maketrans('', '', NOT_ALLOWED_FOR_NAME)
    return original.translate(table)


def remove_diacritics(original: str) -> str:
    """Removes diacritics from the string
    Args:
        original(str): Original string

    Returns(str): String with removed diacritics

    """
    return unidecode(original)


def substitute_spaces(original: str, sub: str = '_') -> str:
    """Substitutes spaces
    Args:
        original(str): Original string
        sub(str): Substitute
    Returns(str): String with substituted spaces
    """
    return sub.join(original.split())


def convert_to_snake(original):
    """Converts an original string to snake case
    Args:
        original(str):  Original String

    Returns(str): Converted string

    """
    snaking = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', original)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', snaking).lower()


def normalize_name(name: str) -> str:
    """Gets a normalized name
    Args:
        name(str): Original name

    Returns(str): Normalized name
    """
    if name is None:
        return name
    name = convert_to_snake(name)
    name = slugify(name)
    name = remove_diacritics(name)
    name = name.lower()
    name = remove_punctuation(name)
    name = substitute_spaces(name)
    return name


def unique_suffix(length=8, context=None):
    if context and context.config['safe_suffixes'] is not True:
        return None
    return secrets.token_urlsafe(length)


def unique_name(name: str, context=None) -> str:
    """Gets an unique name
    Args:
        name(str): Original name
        context(AppContext): Optional context
    Returns(str): Unique name

    """
    suffix = unique_suffix(context=context)
    if suffix is None:
        return name
    return f"{name}_{suffix}"
