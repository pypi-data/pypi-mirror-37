"""
Separate a stream of text into lines.
"""

# Copyright (c) 2018  Peter Pentchev <roam@ringlet.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.


import abc
import functools

from typing import cast, Any, Dict, List, Optional, Tuple

from . import value


class TextSplitter(value.ValueObject, metaclass=abc.ABCMeta):
    """
    Base class for building text splitters: objects that are fed
    characters and spit out fully-formed lines.
    """

    def __init__(self, _data: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the base TextSplitter object, either with data
        from an existing value object, or with the default values -
        an empty buffer, an empty list of lines, a false done flag.
        """
        super(TextSplitter, self).__init__(_data)
        self._data['buf'] = self._data.get('buf', '')
        self._data['lines'] = self._data.get('lines', [])
        self._data['done'] = self._data.get('done', False)

    @property
    def buf(self) -> str:
        """
        Return the buffer of characters not yet forming a line.
        """
        return cast(str, self._data['buf'])

    @property
    def lines(self) -> List[str]:
        """
        Return the buffer of full lines formed so far.
        """
        return cast(List[str], self._data['lines'])

    @property
    def done(self) -> bool:
        """
        Return the "no more incoming text" flag.
        """
        return cast(bool, self._data['done'])

    @abc.abstractmethod
    def add(self, char: Optional[str]) -> 'TextSplitter':
        """
        Process a character or, if passed None, finalize the splitting of
        incoming characters into lines as needed.

        Note: this method only handles the None case; derived classes must
        override it to actually process characters and form lines.
        """
        assert char is None
        data = self._as_dict()
        if data['buf']:
            data['lines'] = data['lines'] + [data['buf']]
            data['buf'] = ''
        data['done'] = True
        return type(self)(_data=data)

    def add_string(self, text: str) -> 'TextSplitter':
        """
        Process all the characters in the specified string.
        """
        return functools.reduce(lambda spl, char: spl.add(char),
                                text, self)

    def pop_lines(self) -> Tuple['TextSplitter', List[str]]:
        """
        Return a tuple with two elements:
        - an object with the same incomplete line buffer, but
          without the accumulated full lines
        - the full lines accumulated so far
        """
        if not self.lines:
            return (self, [])

        data = self._as_dict()
        lines = data['lines']
        data['lines'] = []
        return (type(self)(_data=data), lines)

    @abc.abstractmethod
    def __str__(self) -> str:
        return '{tname}: {ln} lines + {lbuf} characters, {sdone}done' \
               .format(tname=type(self).__name__,
                       ln=len(self.lines), lbuf=len(self.buf),
                       sdone='' if self.done else 'not ')

    def __repr__(self) -> str:
        data = self._as_dict()
        return '{tname}({data})' \
            .format(tname=type(self).__name__,
                    data=', '.join(['{var}={val}'.format(var=var,
                                                         val=repr(data[var]))
                                    for var in sorted(data.keys())]))


class UniversalNewlines(TextSplitter):
    """
    Split a string into text lines in a manner similar to the file class's
    universal newlines mode: detect LF, CR/LF, and bare CR line terminators.
    """

    def __init__(self,
                 preserve: Optional[bool] = None,
                 _data: Optional[Dict[str, Any]] = None
                 ) -> None:
        """
        Initialize a UniversalNewlines splitter object with the specified
        "preserve the line terminators in the returned lines" flag.
        """
        if preserve is None:
            preserve = False

        super(UniversalNewlines, self).__init__(_data)
        self._data['preserve'] = self._data.get('preserve', preserve)
        self._data['was_cr'] = self._data.get('was_cr', False)

    @property
    def preserve(self) -> bool:
        """
        Return the "preserve line terminators in returned lines" flag.
        """
        return cast(bool, self._data['preserve'])

    @property
    def was_cr(self) -> bool:
        """
        Return the "was the last character a CR" flag.
        """
        return cast(bool, self._data['was_cr'])

    def add(self, char: Optional[str]) -> TextSplitter:
        """
        Add a character to the object's buffer and split out a line if
        needed depending on the character being CR, LF, and the previous
        state of the buffer (e.g. detecting CR/LF combinations).
        """

        def newline(data: Dict[str, Any], eol: str) -> None:
            """
            Turn the accumulated buffer into a new line and reset
            the "last character was a CR" flag.
            """
            line = data['buf'] + (eol if data['preserve'] else '')
            data['lines'] = data['lines'] + [line]
            data['buf'] = ''
            data['was_cr'] = False

        if char is None:
            if self.was_cr:
                data = self._as_dict()
                newline(data, '\r')
                return type(self)(_data=data).add(char)
            return super(UniversalNewlines, self).add(char)

        assert not self.done
        data = self._as_dict()
        if data['was_cr']:
            if char == '\n':
                newline(data, '\r\n')
            else:
                newline(data, '\r')
                return type(self)(_data=data).add(char)
        elif char == '\n':
            newline(data, '\n')
        elif char == '\r':
            data['was_cr'] = True
        else:
            data['buf'] = data['buf'] + char

        return type(self)(_data=data)

    def __str__(self) -> str:
        return 'UniversalNewlines: {ln} lines + {lbuf} characters, ' \
               '{sdone} done, {spres}preserve ' \
               .format(ln=len(self.lines), lbuf=len(self.buf),
                       sdone='' if self.done else 'not ',
                       spres='' if self.preserve else 'do not ')


class NullSplitter(TextSplitter):
    """
    Do not split the text at all.
    """
    def add(self, char: Optional[str]) -> TextSplitter:
        """
        Add a character to the object's buffer without any checks for
        line terminators since no splitting is done.
        """
        if char is None:
            return super(NullSplitter, self).add(char)

        assert not self.done

        data = self._as_dict()
        data['buf'] = data['buf'] + char
        return type(self)(_data=data)

    def __str__(self) -> str:  # pylint: disable=useless-super-delegation
        return super(NullSplitter, self).__str__()


class FixedEOLSplitter(TextSplitter):
    r"""
    Split a string into lines using a fixed line separator possibly
    consisting of more than one character, e.g. '\r\n'.
    """

    def __init__(self,
                 eol: Optional[str] = None,
                 _data: Optional[Dict[str, Any]] = None
                 ) -> None:
        """
        Initialize a FixedEOLSplitter object with the specified separator.
        """
        if eol is None:
            eol = '\n'

        super(FixedEOLSplitter, self).__init__(_data)
        self._data['eol'] = self._data.get('eol', eol)
        self._data['in_eol'] = self._data.get('in_eol', 0)

    @property
    def eol(self) -> str:
        """
        Return the sequence of characters used as a line separator.
        """
        return cast(str, self._data['eol'])

    def add(self, char: Optional[str]) -> TextSplitter:
        """
        Process a new character, checking whether it is part of
        an already-started line separator, of a newly-started one,
        or just a normal text character.
        """
        if char is None:
            data = self._as_dict()
            if data['in_eol'] > 0:
                data['buf'] = data['buf'] + data['eol'][:data['in_eol']]
                data['in_eol'] = 0
                return type(self)(_data=data).add(char)
            return super(FixedEOLSplitter, self).add(char)

        assert not self.done
        data = self._as_dict()
        if char == data['eol'][data['in_eol']]:
            data['in_eol'] = data['in_eol'] + 1
            if data['in_eol'] == len(data['eol']):
                data['lines'] = data['lines'] + [data['buf']]
                data['buf'] = ''
                data['in_eol'] = 0
        elif data['in_eol'] > 0:
            data['buf'] = data['buf'] + data['eol'][0]
            to_add = data['eol'][1:data['in_eol']] + char
            data['in_eol'] = 0
            nspl = type(self)(_data=data)  # type: TextSplitter
            for add_char in to_add:
                nspl = nspl.add(add_char)
            return nspl
        else:
            data['buf'] = data['buf'] + char
        return type(self)(_data=data)

    def __str__(self) -> str:
        return '{tname}: {ln} lines + {lbuf} characters, {sdone}done, ' \
               'eol {eol}' \
               .format(tname=type(self).__name__,
                       ln=len(self.lines), lbuf=len(self.buf),
                       sdone='' if self.done else 'not ', eol=repr(self.eol))


def get_dwim_splitter(newline: Optional[str] = None) -> TextSplitter:
    """
    Easily choose a splitter class in a manner similar to open().
    If None is passed for the newline parameter, universal newlines mode
    will be enabled and the line terminators will not be present in
    the returned lines.  If newline is an empty string, universal newlines
    mode is enabled, but the line terminators will be preserved.
    If newline has any other value, it is used as a line terminator and
    stripped from the returned lines.
    """
    if newline is None:
        return UniversalNewlines()
    if newline == '':
        return UniversalNewlines(preserve=True)
    return FixedEOLSplitter(eol=newline)
