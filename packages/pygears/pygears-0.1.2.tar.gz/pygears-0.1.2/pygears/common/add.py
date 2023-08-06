import operator
from functools import reduce

from pygears import alternative, gear, module
from pygears.conf import safe_bind
from pygears.core.intf import IntfOperPlugin
from pygears.typing import Int, Integer, Uint
from pygears.util.hof import oper_tree
from pygears.util.utils import gather


def add_type(dtypes):
    max_len = max(int(d) for d in dtypes)
    length = max_len + len(dtypes) - 1

    if (all(issubclass(d, Uint) for d in dtypes)):
        return Uint[length]

    return Int[length]


@gear(svgen={'svmod_fn': 'add.sv'}, enablement=b'len(din) == 2')
async def add(*din: Integer,
              din0_signed=b'typeof(din0, Int)',
              din1_signed=b'typeof(din1, Int)') -> b'add_type(din)':
    async with gather(*din) as dout:
        yield module().tout(reduce(operator.add, dout))


@alternative(add)
@gear
def add_vararg(*din, enablement=b'len(din) > 2') -> b'add_type(din)':
    return oper_tree(din, add)


class AddIntfOperPlugin(IntfOperPlugin):
    @classmethod
    def bind(cls):
        safe_bind('gear/intf_oper/__add__', add)
