"""
A trivial base class for immutable value objects.
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


from typing import Any, Dict, Optional


class ValueObject:  # pylint: disable=too-few-public-methods
    """
    A trivial base class for immutable value objects that keep
    their data in a _data dictionary member and should only
    provide access to it through getter properties.
    """

    def __init__(self, _data: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the base ValueObject with the specified _data
        dictionary.
        """
        self._data = _data if _data is not None else {}

    def _as_dict(self) -> Dict[str, Any]:
        """
        An internal-use method that returns a shallow copy of the data
        dictionary so that other objects may be created from it.
        """
        return {k: v for (k, v) in self._data.items()}

    def __eq__(self, other: object) -> bool:
        """
        Compare two value objects for equality: compare the object types,
        keys, and values.
        """
        # pylint: disable=unidiomatic-typecheck,protected-access
        if not isinstance(other, ValueObject):
            return False
        vother = other  # type: ValueObject

        return type(self) == type(vother) and \
            set(self._data.keys()) == set(vother._data.keys()) and \
            all([self._data[k] == vother._data[k] for k in self._data.keys()])
