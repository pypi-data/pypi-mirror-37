import logging
from typing import *

_logger = logging.getLogger(__name__)
T = TypeVar('T')


def swap_keys(dct: Dict[T, Dict[T, T]]) -> Dict[T, Dict[T, T]]:
    """Swaps keys of inner and outer dicts keeping values at their correct places."""
    new_dct = {}
    for key, translations in dct.items():
        for lang, text in translations.items():
            if lang not in new_dct:
                new_dct[lang] = {}
            new_dct[lang][key] = text
    return new_dct


def check_missing_non_regional_languages(d: Dict[str, T], sep: str = '-') -> None:
    """Prints warnings if there is only a country-specific language tag in the dict, but not for the language itself."""
    short_keys = {k.split(sep)[0] for k in d.keys()}
    for key in short_keys:
        if key not in d:
            long_keys = [k for k in d.keys() if k.split(sep)[0] == key]
            _logger.warning("The '{}' key{} found, but '{}' is missing!".format(
                "', '".join(long_keys),
                "s are" if len(long_keys) > 1 else " is",
                key))
