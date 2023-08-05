from amino import do, Do

from ribosome.compute.api import prog
from ribosome.nvim.io.state import NS

from proteome.components.core.tpe import CoreRibosome
from proteome.persistence.buffers import load_persisted_buffers


@prog
@do(NS[CoreRibosome, None])
def load() -> Do:
    yield NS.lift(load_persisted_buffers())


__all__ = ('load',)
