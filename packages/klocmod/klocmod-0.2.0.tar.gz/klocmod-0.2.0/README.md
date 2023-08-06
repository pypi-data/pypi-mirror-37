klocmod -- Kozalo's Localization Module
======================================

*Screw you, gettext! I don't wanna bother of compiling strings into binary files!*

[![Build Status](https://travis-ci.org/kozalosev/klocmod.svg?branch=master)](https://travis-ci.org/kozalosev/klocmod)
[![Documentation Status](https://readthedocs.org/projects/klocmod/badge/?version=latest)](https://klocmod.readthedocs.io/en/latest/?badge=latest)

This module provides a very simple, suboptimal way for localizing your scripts, bots or applications. The advantage is
its simplicity: to supply some sets of different string literals for different languages, you just need a simple JSON or
INI file (or even a dict) fed to the library. After that, the only thing you should take care of is to get an instance
of the dictionary for a specific language and extract messages from it by key values.

All you mostly want is the `LocalizationsContainer` class. In particular, its static method 
`LocalizationsContainer.from_file()` that reads a localization file and returns an instance of the factory. The factory
is supposed to produce instances of the `LanguageDictionary` class. Most likely, you will encounter instances of its
subclass -- the `SpecificLanguageDictionary` class (the base class is only used as a fallback that returns passed key
values back).

Examples of localization files
------------------------------

### JSON (language first)


```json
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
```

### JSON (phrase first)

```json
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
```

### INI

```ini
[DEFAULT]
yes = yes
no = no

[ru-RU]
yes = да
no = нет
```


Code example
------------

```python
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
```
