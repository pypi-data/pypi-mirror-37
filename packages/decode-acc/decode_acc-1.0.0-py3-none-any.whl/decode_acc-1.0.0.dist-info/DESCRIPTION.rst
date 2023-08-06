# An incremental decoder of bytes into characters and lines

## The DecodeAccumulator class

The `DecodeAccumulator` class implements an incremental decoder: an object
that may be fed bytes (one or several at a time) as they are e.g. read
from a network stream or a subprocess's output, and that adds to a result
string as soon as enough bytes have been accumulated to produce a character
in the specified encoding.

Note that `DecodeAccumulator` objects are immutable value objects:
the `add()` method does not modify its invocant, but returns a new
`DecodeAccumulator` object instead.

Sample usage:

    while True:
        bb = subprocess.stdout.read(1024)
        if len(bb) == 0:
            break
        acc = acc.add(bb)
        assert(not acc.done)
        if acc.splitter.lines:
            # at least one full line was produced
            (acc, lines) = acc.pop_lines()
            print('\n'.join(lines)

    if acc.buf:
        print('Leftover bytes left in the buffer!', file=sys.stderr)

    if acc.splitter.buf:
        print('Incomplete line: ' + acc.splitter.buf)

    final = acc.add(None)
    assert(final.splitter.buf == '')
    assert(final.splitter.done)
    assert(final.done)
    if acc.splitter.buf:
        assert(len(final.splitter.lines) == len(acc.splitter.lines) + 1)

## The splitter classes: UniversalNewlines, FixedEOLSplitter, NullSplitter

The `decode_acc.newlines` module provides three classes that may be used to
split a text string into lines in different ways.  The `UniversalNewlines`
class does its best to simulate the "universal newlines" behavior of `file`
objects.  The `FixedEOLSplitter` class uses a specified string as a line
terminator to split on.  The `NullSplitter` class does not do any splitting.

Sample usage:

    spl = newlines.UniversalNewlines()
    for char in input_string:
        spl = spl.add(char)
    spl.add(None)

    for (idx, line) in enumerate(spl.lines):
        print('line {idx}: {line}'.format(idx=idx, line=line))

## License and copyright

    Copyright (c) 2018  Peter Pentchev <roam@ringlet.net>
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:
    1. Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
    OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
    OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
    SUCH DAMAGE.


