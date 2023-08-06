"""
Incrementally decode bytes into strings and lines.
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


import collections

from typing import cast, Any, Dict, Optional, Tuple, Union

from . import value


class DecodeAccumulator(value.ValueObject):
    r"""
    Incrementally decode bytes into strings.

    This class implements an incremental decoder: an object that may be
    fed bytes (one or several at a time) as they are e.g. read from
    a network stream or a subprocess's output, and that adds to a result
    string as soon as enough bytes have been accumulated to produce
    a character in the specified encoding.

    Note that DecodeAccumulator objects are immutable value objects:
    the add() method does not modify its invocant, but returns a new
    DecodeAccumulator object instead.

    Sample usage:

        while True:
            bb = subprocess.stdout.read(1024)
            if len(bb) == 0:
                break
            acc = acc.add(bb)
            assert(not acc.done)
            if acc.decoded:
                # at least one full line was produced
                (acc, text) = acc.pop_decoded()
                print(text, end='')

        acc.add(None)
        if acc.buf:
            print('Leftover bytes left in the buffer!', file=sys.stderr)

        if acc.splitter.buf:
            print('Incomplete line: ' + acc.splitter.buf)

        final = acc.add(None)
        assert(final.done)

    Sample usage with a text splitter, e.g. one from the newlines module:

        spl = newlines.get_dwim_splitter()

        # May be done each time a character is decoded, or just once at
        # the end, or anything in between.
        (acc, text) = acc.pop_decoded()
        spl = spl.add_string(text)

        # Finalize; we won't be needing the accumulator any more...
        spl = spl.add_string(acc.add(None).pop_decoded()[1])
        print('{lc} lines and {ll} leftover characters'
              .format(lc=len(spl.lines), ll=len(spl.buf)))

        # If we don't care that there might be no EOL on the last line,
        # we might as well have finalized the splitter, too, to form
        # one last line:
        spl = spl.add(None)
        print('{lc} lines and {ll} (should be 0) leftover characters'
              .format(lc=len(spl.lines), ll=len(spl.buf)))
        assert len(spl.buf) == 0
    """

    ByteAccumulator = collections.namedtuple('ByteAccumulator',
                                             ['buf', 'decoded'])

    def __init__(self,
                 encoding: Optional[str] = None,
                 _data: Optional[Dict[str, Any]] = None
                 ) -> None:
        """
        Initialize a DecodeAccumulator object with the specified encoding.
        """
        if encoding is None:
            encoding = 'UTF-8'

        super(DecodeAccumulator, self).__init__(_data)
        self._data['encoding'] = self._data.get('encoding', encoding)
        self._data['buf'] = self._data.get('buf',
                                           ''.encode(self._data['encoding']))
        self._data['decoded'] = self._data.get('decoded', '')
        self._data['done'] = self._data.get('done', False)

    @property
    def encoding(self) -> str:
        """
        Return the name of the encoding used to decode text.
        """
        return cast(str, self._data['encoding'])

    @property
    def buf(self) -> bytes:
        """
        Return the buffer of bytes that have not formed a full character yet.
        """
        return cast(bytes, self._data['buf'])

    @property
    def decoded(self) -> str:
        """
        Return the characters decoded so far.
        """
        return cast(str, self._data['decoded'])

    @property
    def done(self) -> bool:
        """
        Return the "no more incremental decoding" flag.
        """
        return cast(bool, self._data['done'])

    def add(self, new_data: Union[bytes, None]) -> 'DecodeAccumulator':
        """
        Add the specified bytes to the internal buffer and try to decode
        as many characters from the buffer as possible.

        If invoked with None as a parameter, finalizes the incremental
        encoding; no more bytes may be added in the future.
        """

        def add_byte(acc: DecodeAccumulator.ByteAccumulator,
                     byte: int
                     ) -> DecodeAccumulator.ByteAccumulator:
            """
            Add a byte to the incremental decoding buffer, try to decode
            a full character; if successful, pass it to the splitter.
            """
            buf = acc.buf + bytes([byte])
            try:
                char = buf.decode(self.encoding)
                buf = ''.encode('us-ascii')
            except UnicodeDecodeError:
                return self.ByteAccumulator(buf=buf,
                                            decoded=acc.decoded)

            return self.ByteAccumulator(buf=''.encode(self.encoding),
                                        decoded=acc.decoded + char)

        if new_data is None:
            data = self._as_dict()
            data['done'] = True
            return type(self)(_data=data)

        assert not self.done
        acc = self.ByteAccumulator(buf=self.buf, decoded=self.decoded)
        for byte in new_data:
            acc = add_byte(acc, byte)

        data = self._as_dict()
        data['buf'] = acc.buf
        data['decoded'] = acc.decoded
        return type(self)(_data=data)

    def pop_decoded(self) -> Tuple['DecodeAccumulator', str]:
        """
        Return a tuple with two elements:
        - an object with the same incremental decoding state, but
          without the accumulated decoded characters
        - the text decoded so far
        """
        data = self._as_dict()
        text = data['decoded']
        data['decoded'] = ''
        return (
            type(self)(_data=data),
            text
        )

    def __str__(self) -> str:
        return 'DecodeAccumulator: encoding "{enc}", {rln} raw bytes, ' \
               '{rdec} decoded characters, {sdone}done' \
               .format(enc=self.encoding, rln=len(self.buf),
                       rdec=len(self.decoded),
                       sdone='' if self.done else 'not ')

    def __repr__(self) -> str:
        data = self._as_dict()
        return 'DecodeAccumulator({data})' \
            .format(data=', '.join(['{var}={val}'.format(var=var,
                                                         val=repr(data[var]))
                                    for var in sorted(data.keys())]))
