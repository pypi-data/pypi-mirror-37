Alphanumeric unique code generator
==================================

This module generates unique consecutive alphanumeric codes of specified size.
A comment can be associated with a code on request.

Requirements
------------

- python >= 2.7
- SQLAchemy

Package depencies are included in alphanum_code package and will be automatically installed.
For more details,  see `requirements.txt`.

Install
-------

Install from PyPI:

    pip install alphanum_code

Install from source:

```bash
git clone https://github.com/ylaizet/alphanum_code
cd alphanum_code
pip install -e .
```

Usage 
-----

    >>> from alphanum_code import AlphaNumCodeManager
    >>> dbname = "sqlite:///test_alphanum.sqlite"
    >>> manager = AlphaNumCodeManager(dbname)
    >>> first_code = manager.next_code("with comment")
    >>> print("my first code:", first_code)

Notes
-----

- Alphanumeric order is digits then letters : `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ`.
- Letters in the alphanumeric code are UPPERCASE.

Tips
----

At `manager` instanciation, you can set:

- `code_size` to specify the lenght of the code you want to generate each time
- `init_code` to specify the starting point for code generation

Test
----

Install Pytest

    pip install pytest

Run test from base directory

    python -m pytest tests/
