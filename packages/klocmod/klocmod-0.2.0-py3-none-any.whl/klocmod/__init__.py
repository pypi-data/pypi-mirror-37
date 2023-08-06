"""
*Screw you, gettext! I don't wanna bother of compiling strings into binary files!*

This module provides a very simple, suboptimal way for localizing your scripts, bots or applications. The advantage is
its simplicity: to supply some sets of different string literals for different languages, you just need a simple JSON
or INI file (or even a dict) fed to the library. After that, the only thing you should take care of is to get an
instance of the dictionary for a specific language and extract messages from it by key values.

All you mostly want is the :py:class:`LocalizationsContainer` class. In particular, its static method
:py:func:`LocalizationsContainer.from_file` that reads a localization file and returns an instance of the factory. The
factory is supposed to produce instances of the :py:class:`LanguageDictionary` class. Most likely, you will encounter
instances of its subclass -- the :py:class:`SpecificLanguageDictionary` class (the base class is only used as a fallback
that returns passed key values back).

Examples of localization files
==============================

JSON (language first)
---------------------

.. code-block:: json

    {
      "en": {
        "yes": "yes",
        "no": "no"
      },
      "ru-RU": {
        "yes": "да",
        "no": "нет"
      }
    }

JSON (phrase first)
-------------------

.. code-block:: json

    {
      "yes": {
        "en": "yes",
        "ru-RU": "да"
      },
      "no": {
        "en": "no",
        "ru-RU": "нет"
      }
    }

INI
---

.. code-block:: ini

    [DEFAULT]
    yes = yes
    no = no

    [ru-RU]
    yes = да
    no = нет


Code example
============

.. code-block:: python3

    from klocmod import LocalizationsContainer

    localizations = LocalizationsContainer.from_file("localization.json")
    ru = localizations.get_lang("ru")
    # or
    en = localizations.get_lang()    # get default language
    # then
    print(ru['yes'])    # output: да
    # alternative ways to get a specific phrase:
    localizations.get_phrase("ru-RU", "no")
    localizations['ru-RU']['no']
"""


import logging
import json
import configparser
from typing import *
from pathlib import PurePath, Path

from .internals import swap_keys, check_missing_non_regional_languages
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__all__ = ['LanguageDictionary', 'SpecificLanguageDictionary', 'LocalizationsContainer', 'InvalidLocalizationFileError']
_logger = logging.getLogger(__name__)


class LanguageDictionary:
    """
    The base class for dict-like objects containing phrases for a particular language. Usually used as a fallback since
    just returns keys back (printing a warning into the log, of course).

    You shouldn't instantiate objects of this class on your own. Use the :py:class:`LocalizationsContainer` class
    instead.

    The class supports equality testing based on the :py:attr:`name` property. Note that if the other object is not
    an instance of the :py:class:`LanguageDictionary` class, a :py:exc:`TypeError` exception will be thrown.
    """

    def __init__(self, name: str) -> None:
        self._logger = _logger.getChild(self.__class__.__name__ + '.' + name)
        self._name = name

    def __contains__(self, item: str) -> bool:
        return True

    def __getitem__(self, item: str) -> str:
        self._logger.warning("Localized phrase not found at all: %s" % item)
        return item

    @property
    def name(self) -> str:
        """The name of the locale ('ru-RU', 'en', etc.)"""
        return self._name

    def __eq__(self, other) -> bool:
        if not isinstance(other, LanguageDictionary):
            raise TypeError("Incomparable types!")
        return self._name == other._name


class SpecificLanguageDictionary(LanguageDictionary):
    """
    A concrete implementation of :py:class:`LanguageDictionary` that consists of two dicts: one of them is considered as
    primary one and the other as spare. When you're trying to get some localized phrase by a key, the primary dict is
    used for searching first. If there is no such a key there, the search continues in the spare dict. Finally, if there
    is no such a phrase, the key itself is returned by the base class.

    Using instances of this class it's possible to make chains of language dictionaries. For example, you can create the
    following chain of searching: ``fr-CA -> fr -> en (default language) -> fallback``

    In fact, this approach is used for localization files parsed by the :py:class:`LocalizationContainer` class.

    All missing phrases will be present in the log.

    :param name: a language tag
    :param primary_dict: an actual dict of localized strings
    :param spare_dict: an instance of :py:class:`LanguageDictionary` that is used as a fallback
    """

    def __init__(self, name: str, primary_dict: Dict[str, str], spare_dict: LanguageDictionary) -> None:
        super().__init__(name)
        self._primary_dict = primary_dict
        self._spare_lang_dict = spare_dict

    def __getitem__(self, item: str) -> str:
        if item in self._primary_dict:
            return self._primary_dict[item]
        elif item in self._spare_lang_dict:
            warn_msg = "Localized phrase for {} not found, used for {}.".format(self.name, self._spare_lang_dict.name)
            self._logger.warning(warn_msg)
            return self._spare_lang_dict[item]
        else:
            return super()[item]

    def __eq__(self, other) -> bool:
        if not isinstance(other, LanguageDictionary):
            raise TypeError("Incomparable types!")
        if not isinstance(other, SpecificLanguageDictionary):
            return False
        return self._primary_dict == other._primary_dict and self._spare_lang_dict == other._spare_lang_dict


class LocalizationsContainer:
    """
    A factory of :py:class:`LanguageDictionary` instances. Call the :py:meth:`LocalizationContainer.from_file` static
    method to get the instance of the container. Then you can use the :py:meth:`LocalizationContainer.get_lang` method
    to create instances of specific languages (:py:class:`LanguageDictionary`).

    :param dct: see examples in the module description
    :param default_lang: what language key will be used as a fallback
    """

    def __init__(self, dct: Dict[str, Dict[str, str]], default_lang: str = 'en') -> None:
        if default_lang in dct.keys():
            pass
        elif default_lang in next(iter(dct.values())):
            dct = swap_keys(dct)
        else:
            raise ValueError("No default language was found.")
        self._primary_dict = {k.replace('_', '-').lower(): v for k, v in dct.items()}    # normalize language tags
        check_missing_non_regional_languages(self._primary_dict)
        self._spare_lang_dct = SpecificLanguageDictionary(default_lang, self._primary_dict[default_lang],
                                                          LanguageDictionary(default_lang))

    @classmethod
    def from_file(cls, path: Union[PurePath, str], default_lang: str = 'en') -> 'LocalizationsContainer':
        """
        A factory method that reads a given file and returns an instance of the :py:class:`LocalizationsContainer`
        class.

        Currently supported formats are **JSON** and **INI**.

        :param path: a path to the localization file
        :param default_lang: what language key will be used as a fallback
        :return: an instance of :py:class:`LocalizationsContainer`
        """
        path = Path(path)
        with path.open('r', encoding="UTF-8") as f:
            if path.suffix == ".json":
                try:
                    dct = json.load(f)
                except json.JSONDecodeError as err:
                    raise InvalidLocalizationFileError("Invalid JSON file.", path.name, err)
            elif path.suffix == ".ini":
                parser = configparser.ConfigParser()
                try:
                    parser.read_file(f)
                except configparser.ParsingError as err:
                    raise InvalidLocalizationFileError("Invalid INI file.", path.name, err)
                dct = {section: dict(parser[section]) for section in parser.sections()}
                dct[default_lang] = dict(parser[parser.default_section])
            elif path.suffix in (".yml", ".yaml"):
                import yaml    # extra dependency
                try:
                    dct = yaml.safe_load(f)
                except yaml.YAMLError as err:
                    raise InvalidLocalizationFileError("Invalid YAML file.", path.name, err)
            else:
                raise InvalidLocalizationFileError("Not supported file type: " + path.suffix, path.name)
        try:
            return cls(dct, default_lang)
        except ValueError as err:
            raise InvalidLocalizationFileError(str(err), path.name, err)

    def get_language(self, language: str, country: str = None) -> LanguageDictionary:
        """
        Returns a set of phrases for some certain language.

        :param language: 2 character code of the language
        :param country: 2 character code of the country (may be omitted)
        :return: an instance of :py:class:`LanguageDictionary`
        """
        if language in self._primary_dict and language != self._spare_lang_dct.name:
            lang = SpecificLanguageDictionary(language, self._primary_dict[language], self._spare_lang_dct)
        else:
            lang = self._spare_lang_dct
        if not country:
            return lang
        lang_tag = "{}-{}".format(language.lower(), country.lower())
        if lang_tag in self._primary_dict:
            return SpecificLanguageDictionary(lang_tag, self._primary_dict[lang_tag], lang)
        else:
            return lang

    def get_lang(self, lang_tag: str = None) -> LanguageDictionary:
        """
        The same as :py:meth:`get_language` but takes either hyphen-separated and underscore-separated language tags as
        a one entry. Returns the default language if the desired language doesn't present in the localization container
        (or if ``lang_tag`` is *None*).

        :param lang_tag: language tags such as "en-US", "en_AU" or just "en"
        :return: an instance of :py:class:`LanguageDictionary`
        """
        if not lang_tag:
            return self._spare_lang_dct
        lang_tag_parts = lang_tag.replace('_', '-').split('-')
        if len(lang_tag_parts) == 2:
            return self.get_language(language=lang_tag_parts[0], country=lang_tag_parts[1])
        elif len(lang_tag_parts) == 1:
            return self.get_language(language=lang_tag)
        else:
            raise ValueError("Invalid language tag: '{}'".format(lang_tag))

    def get_phrase(self, lang_tag: str, key: str) -> str:
        """
        A shortcut for :py:meth:`get_lang` that let you retrieve only a one phrase at once, not a whole dictionary.

        :param lang_tag: "en-US", "en_AU" or just "en"
        :param key: a key identified the phrase in the dictionary
        :return: the locale-specific phrase
        """
        return self.get_lang(lang_tag)[key]

    def __getitem__(self, lang_tag: str) -> LanguageDictionary:
        return self.get_lang(lang_tag)

    def __eq__(self, other) -> bool:
        if not isinstance(other, LocalizationsContainer):
            raise TypeError("Incomparable types!")
        return self._primary_dict == other._primary_dict and self._spare_lang_dct == other._spare_lang_dct


class InvalidLocalizationFileError(Exception):
    """
    An exception that is thrown when any error occurred while parsing some localization file.

    :param message: a human-readable message describing the error
    :param file_path: a path to the localization file
    :param nested_exc: another exception that caused this one, if present
    """

    def __init__(self, message: str, file_path: Union[PurePath, str], nested_exc: Exception = None) -> None:
        super().__init__(message)
        self._file_path = Path(file_path)
        self._nested_exc = nested_exc

    @property
    def file_path(self) -> Path:
        """A full path to the localization file caused the error."""
        return self._file_path

    @property
    def filename(self) -> str:
        """The name of the localization file caused the error."""
        return self._file_path.name

    @property
    def nested_exception(self) -> Exception:
        """Another exception that caused this one."""
        return self._nested_exc
