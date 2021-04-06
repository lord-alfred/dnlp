import re

from ftfy import fix_text

from dnlp.constants import (
    EMAIL_REGEX,
    LINEBREAK_REGEX,
    NONBREAKING_SPACE_REGEX,
    NUMBERS_REGEX,
    PUNCT_TRANSLATE_UNICODE,
    SHORT_URL_REGEX,
    URL_REGEX,
)


def preprocess_text(text):
    """Based on `textacy.preprocess_text` method"""
    # small speedup
    text = text.strip()
    if not text:
        return text

    text = fix_bad_unicode(text, normalization="NFC")

    # custom `replace_with` values for more detectable results
    text = replace_urls(text, replace_with=' ')
    text = replace_emails(text, replace_with=' ')
    text = replace_numbers(text, replace_with=' ')

    text = remove_punct(text)
    text = text.lower()
    text = normalize_whitespace(text)

    # fastText work only with 1 line of text
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')

    return text.strip()


def fix_bad_unicode(text, normalization="NFC"):
    """
    Fix unicode text that's "broken" using `ftfy <http://ftfy.readthedocs.org/>`_;
    this includes mojibake, HTML entities and other code cruft,
    and non-standard forms for display purposes.

    Args:
        text (str): raw text
        normalization ({'NFC', 'NFKC', 'NFD', 'NFKD'}): if 'NFC',
            combines characters and diacritics written using separate code points,
            e.g. converting "e" plus an acute accent modifier into "é"; unicode
            can be converted to NFC form without any change in its meaning!
            if 'NFKC', additional normalizations are applied that can change
            the meanings of characters, e.g. ellipsis characters will be replaced
            with three periods

    Returns:
        str
    """
    return fix_text(text, normalization=normalization)


def replace_urls(text, replace_with="*URL*"):
    """Replace all URLs in ``text`` str with ``replace_with`` str."""
    return URL_REGEX.sub(
        replace_with, SHORT_URL_REGEX.sub(replace_with, text)
    )


def replace_emails(text, replace_with="*EMAIL*"):
    """Replace all emails in ``text`` str with ``replace_with`` str."""
    return EMAIL_REGEX.sub(replace_with, text)


def replace_numbers(text, replace_with="*NUMBER*"):
    """Replace all numbers in ``text`` str with ``replace_with`` str."""
    return NUMBERS_REGEX.sub(replace_with, text)


def remove_punct(text, marks=None):
    """
    Remove punctuation from ``text`` by replacing all instances of ``marks``
    with whitespace.

    Args:
        text (str): raw text
        marks (str): If specified, remove only the characters in this string,
            e.g. ``marks=',;:'`` removes commas, semi-colons, and colons.
            Otherwise, all punctuation marks are removed.

    Returns:
        str

    Note:
        When ``marks=None``, Python's built-in :meth:`str.translate()` is
        used to remove punctuation; otherwise, a regular expression is used
        instead. The former's performance is about 5-10x faster.
    """
    if marks:
        return re.sub("[{}]+".format(re.escape(marks)), " ", text, flags=re.UNICODE)
    else:
        return text.translate(PUNCT_TRANSLATE_UNICODE)


def normalize_whitespace(text):
    """
    Given ``text`` str, replace one or more spacings with a single space, and one
    or more linebreaks with a single newline. Also strip leading/trailing whitespace.
    """
    return NONBREAKING_SPACE_REGEX.sub(
        " ", LINEBREAK_REGEX.sub(r"\n", text)
    ).strip()
