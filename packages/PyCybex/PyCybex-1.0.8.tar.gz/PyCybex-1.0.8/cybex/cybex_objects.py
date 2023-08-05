import pdb
from graphenebase.types import (
    Uint8, Int16, Uint16, Uint32, Uint64,
    Varint32, Int64, String, Bytes, Void,
    Array, PointInTime, Signature, Bool,
    Set, Fixed_array, Optional, Static_variant,
    Map, Id, VoteId,
    ObjectId as GPHObjectId
)
from .cybex_types import (
    Ripemd160
)

from collections import OrderedDict
from graphenebase.objects import GrapheneObject, isArgsThisClass
from bitsharesbase.account import PublicKey

class TransferExtensions(Set):
    def __init__(self, *args, **kwargs):
        # Extensions #############################
        class Vesting_ext(GrapheneObject):
            def __init__(self, kwargs): 
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('vesting_period', Uint64(kwargs['vesting_period'])),
                        ('public_key', PublicKey(kwargs['public_key'], prefix = 'CYB'))
                    ]))

        class Xfer_to_name_ext(GrapheneObject):
            def __init__(self, kwargs):
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('name', String(kwargs['name'])),
                        ('asset_sym', String(kwargs['asset_sym'])),
                        ('fee_asset_sym', String(kwargs['fee_asset_sym'])),
                        ('hw_cookie1', Uint8(kwargs['hw_cookie1'])),
                        ('hw_cookie2', Uint8(kwargs['hw_cookie2']))
                    ]))
        # End of Extensions definition ###########

        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

        a = []

        sorting = sorted(kwargs, key=lambda x: x[0])
        for ext in sorting:
            if ext[0] == 1:
                a.append(Static_variant(
                    Vesting_ext(ext[1]),
                    ext[0])
                )
            elif ext[0] == 4:
                a.append(Static_variant(
                    Xfer_to_name_ext(ext[1]),
                    ext[0])
                )
            else:
                raise NotImplementedError("Extension {} is unknown".format(ext[0]))

        super().__init__(a)

class AssetIssueExtensions(Set):
    def __init__(self, *args, **kwargs):
        # Extensions #############################
        class Vesting_ext(GrapheneObject):
            def __init__(self, kwargs): 
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('vesting_period', Uint64(kwargs['vesting_period'])),
                        ('public_key', PublicKey(kwargs['public_key'], prefix = 'CYB'))
                    ]))
        # End of Extensions definition ###########

        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

        a = []

        sorting = sorted(kwargs, key=lambda x: x[0])
        for ext in sorting:
            if ext[0] == 1:
                a.append(Static_variant(
                    Vesting_ext(ext[1]),
                    ext[0])
                )
            else:
                raise NotImplementedError("Extension {} is unknown".format(ext[0]))

        super().__init__(a)

class LimitOrderCancelExtensions(Set):
    def __init__(self, *args, **kwargs):
        # Extensions ############################
        class Cancel_trx_id_ext(GrapheneObject):
            def __init__(self, kwargs):
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(OrderedDict([
                        ('trx_id', Ripemd160(kwargs['trx_id']))
                    ]))
        # End of Extensions definition ##########
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
        a = []
        ext = kwargs[0]
        assert ext[0] == 6
        a.append(Static_variant(
            Cancel_trx_id_ext(ext[1]),
            ext[0]
        ))
        super().__init__(a)
