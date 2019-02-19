import os
import struct
from collections import OrderedDict

from . import ReaderBase
from .exceptions import ReaderError

class PEIReader(ReaderBase):
    def __init__(self, filepath):
        super(PEIReader, self).__init__(filepath, rb=True)

        self._header()
        self._fd.read(3) # data starts after 3 bytes

        self._datatype_bytes = {
            'as': 1,
            'by': 1,
            'db': 8,
            'fl': 4,
            'in': 2,
            'li': 4,
            'si': 1,
            'wd': 2
        }
        # https://docs.python.org/3/library/struct.html#format-characters
        self._datatype_conv = {
            'as': 's',
            'by': 'b',
            'db': 'd',
            'fl': 'f',
            'in': 'h',
            'li': 'i',
            'si': 'h',
            'wd': 'h'
        }

    def _header(self):
        """Read header part
        """
        inRecordDef = False
        recordDef = OrderedDict()
        while True:
            line = self._fd.readline()
            if line.startswith(b'END'):
                break
            if line.startswith(b'RECORDPEI definition'):
                inRecordDef = True
                continue
            if line.startswith(b'BEGIN'):
                continue
            # read record definition
            if inRecordDef:
                item = line.rstrip(b'\r\n').split(b',')
                recordDef[item[0].decode('utf-8')] = {
                    'length' : int(item[1]),
                    'type': item[2].decode('utf-8'),
                    'multiplier': float(item[3]) if item[3] not in (b'0', b'1') else None,
                    'unit': item[5].decode('utf-8') if item[5] != b'0' else None,
                    'alias': item[6].decode('utf-8')
                }

        self._recordDef = recordDef

    def _next_data_item(self):
        """Read next data item.
        """
        # check EOF
        data = self._fd.read(1)
        if not data:
            return None
        self._fd.seek(-1, 1) # return previously read byte

        # parse record
        item = OrderedDict()
        for name, rdef in self._recordDef.items():
            dtype = self._datatype_conv[rdef['type']]
            nbytes = rdef['length'] * self._datatype_bytes[rdef['type']]
            if dtype == 's':
                dtype = '{}s'.format(nbytes)
            value = struct.unpack(
                dtype, self._fd.read(nbytes)
            )[0]
            if rdef['multiplier']:
                value *= rdef['multiplier']
            if self._datatype_conv[rdef['type']] == 's':
                value = value.decode('utf-8').strip(' ')
            item[name] = value

        return item

    def count(self):
        """Count data items.

        :todo:
        """
        return -1

    def _reset(self):
        """Reset reading.
        """
        pass # disable for __iter__
