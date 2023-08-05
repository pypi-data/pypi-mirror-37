from amino import List

from ribosome.config.component import Component
from ribosome.rpc.api import rpc
from ribosome.rpc.data.prefix_style import Full

from proteome.components.core.data.core_data import CoreData
from proteome.components.core.compute.init import init
from proteome.components.core.compute.add import add
from proteome.components.core.compute.stage2 import stage2
from proteome.components.core.compute.stage4 import stage4
from proteome.components.core.compute.save import save
from proteome.components.core.compute.load import load

core: Component = Component.cons(
    'core',
    state_type=CoreData,
    rpc=List(
        rpc.write(init),
        rpc.write(add),
        rpc.write(stage2).conf(prefix=Full()),
        rpc.write(stage4).conf(prefix=Full()),
        rpc.write(save),
        rpc.write(load),
    ),
)

__all__ = ('core',)
