import ctypes as ct
from coreir.base import CoreIRType
from coreir.lib import libcoreir_c

class COREMetaData(ct.Structure):
    pass


COREMetaData_p = ct.POINTER(COREMetaData)


class MetaData(CoreIRType):
    def add_metadata(self, key, value):
        libcoreir_c.COREMetaDataAddStr(self.ptr, str.encode(key),
                                               str.encode(value))
