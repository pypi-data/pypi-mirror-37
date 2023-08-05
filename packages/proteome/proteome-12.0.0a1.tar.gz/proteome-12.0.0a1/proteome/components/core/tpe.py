from proteome.components.core.data.core_data import CoreData
from proteome.data.env import Env
from proteome.config.component import ProteomeComponent

from ribosome.compute.ribosome import Ribosome

CoreRibosome = Ribosome[Env, ProteomeComponent, CoreData]

__all__ = ('CoreRibosome',)
