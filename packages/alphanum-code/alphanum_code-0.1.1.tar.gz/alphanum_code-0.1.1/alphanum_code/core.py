#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Alphanumeric unique consecutive code generator.

Usage:

    >>> from alphanum_code import AlphaNumCodeManager
    >>> dbname = "sqlite:///test_alphanum.sqlite"
    >>> manager = AlphaNumCodeManager(dbname)
    >>> first_code = manager.next_code("with comment")
    >>> print("my first code:", first_code)
"""


__author__ = "Yec'han Laizet"

__all__ = ['AlphaNumCodeManager']


import datetime
import string
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


class AlphaNumCodeManager(object):
    """AlphaNum code manager."""

    Base = declarative_base()
    Alphabet = string.digits + string.ascii_uppercase

    def __init__ (self, dbname, code_size=4, init_code=None):
        """Class initialiser."""
        self.engine = create_engine(dbname)
        self.code_size = code_size
        self.init_code = init_code
        if init_code is None:
            self.init_code = AlphaNumCodeManager.Alphabet[0] * self.code_size
        self.alphabet_map = {j: i for i, j in enumerate(AlphaNumCodeManager.Alphabet)}
        self.alphabet_size = len(self.alphabet_map)

        if len(self.init_code) != self.code_size:
            raise ValueError("code_size (%d) does not fit init_code length (%d)" % (self.code_size, len(self.init_code)))

        AlphaNumCodeManager.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        last_record = self._get_last_record()
        if last_record is not None:
            if len(last_record) != self.code_size:
                raise ValueError("code_size (%d) does not fit length of existing codes (%d) in %s" % (self.code_size, len(last_record), dbname))

    def _calculate_next_code(self, code):
        """Return newly calculated code based on provided code.

        Args:
            code (str): code used to calculate the next one

        Returns:
            str: calculated new code
        """
        reverse_new_code_ints = [self.alphabet_map[char] for char in code[::-1]]
        reverse_new_code_ints[0] += 1
        for i, new_code_int in enumerate(reverse_new_code_ints):
            if new_code_int >= self.alphabet_size:
                if i >=  self.code_size - 1:
                    raise StopIteration("Last code reached")
                else:
                    reverse_new_code_ints[i] = 0
                    reverse_new_code_ints[i + 1] += 1
        next_code = [AlphaNumCodeManager.Alphabet[new_code_int] for new_code_int in reverse_new_code_ints[::-1]]
        return "".join(next_code)

    def _get_last_record(self):
        """Get last record.

        Returns:
            str: last registered code
        """
        query = self.session.query(AlphaNumCode).order_by(AlphaNumCode.id.desc()).first()
        return query

    def next_code(self, info=None):
        """Returns new code based on last registered code in db.

        Args:
            info (str): metadata to store in db along with new code

        Returns:
            str: new code
        """
        last_code_object = self._get_last_record()
        if last_code_object is None:
            new_code = self.init_code
        else:
            new_code = self._calculate_next_code(last_code_object.code)
        new_date = datetime.datetime.now().isoformat()
        next_alphanum_code = AlphaNumCode(code=new_code, date=new_date, info=info)
        self.session.add(next_alphanum_code)
        self.session.commit()
        return new_code


class AlphaNumCode(AlphaNumCodeManager.Base):
     __tablename__ = 'codes'

     id = Column(Integer, primary_key=True, autoincrement=True)
     code = Column(String, unique=True)
     date = Column(String)
     info = Column(String)

     def __repr__(self):
        return "<Code(id='%s', code='%s', date='%s', info='%s')>" % (self.id, self.code, self.date, self.info)
