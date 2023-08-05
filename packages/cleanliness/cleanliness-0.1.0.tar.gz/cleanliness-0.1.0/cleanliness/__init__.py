# coding: utf-8
"""Initialization code for Cleanliness."""
import regex

SINGLE_QUOTE_REGEX = regex.compile(r"(\u0027|\u0060|\u00b4|\u2019|‘)", flags=regex.IGNORECASE)
DOUBLE_QUOTE_REGEX = regex.compile(r"(\\?)(\"|\u00ab|\u00bb|\u201c|\u201f|\u201d|„)", flags=regex.IGNORECASE)
DASH_REGEX = regex.compile(r'(-|\u2010|\u2011|\u2012|\u2013|\u2014|\u2015|\u2212)', regex.UNICODE)


def normalize(text):
    """
    Normalize specified text.

    Various kinds of dashes and hyphens are normalized to '-'.
    Various kinds of single quotes are normalized to "'".
    Various kinds of double quotes are normalized to '"'.
    Various kinds of non-linebreaking whitespace are normalized to ' '.
    Various kinds of linebreaking whitespace are normalized to newline.
    Multiple continuous whitespace characters are squashed to a single whitespace.
    """
    text = normalize_dashes((text))
    text = normalize_single_quotes(text)
    text = normalize_double_quotes(text)
    text = normalize_whitespace(text)
    return text


def normalize_dashes(text):
    """Normalize various kinds of dashes and hyphens to '-'."""
    return DASH_REGEX.sub("-", text)


def normalize_single_quotes(text):
    """Normalize various kinds of single quotes to "'"."""
    return SINGLE_QUOTE_REGEX.sub("'", text)


def normalize_double_quotes(text):
    """Normalize various kinds of double quotes to '"'."""
    return DOUBLE_QUOTE_REGEX.sub('"', text)


def normalize_whitespace(text):
    """Multiple continuous whitespace characters are squashed to a single whitespace."""
    text = regex.sub(r"(\n[\s]*)+", "\n", text).strip()
    text = regex.sub(r"[ \t\r\f\v]+", " ", text).strip()
    return text
