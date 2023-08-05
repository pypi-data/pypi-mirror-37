from amino import List, Map

from ribosome.config.config import Config

from proteome.data.env import Env
from proteome.components.core.config import core
from proteome.components.core.compute.init import init

proteome_config: Config = Config.cons(
    name='proteome',
    prefix='pro',
    state_ctor=Env.cons,
    components=Map(core=core),
    core_components=List('core'),
    init=init,
)

__all__ = ('proteome_config')
