from amino import do, Do

from ribosome.compute.api import prog
from ribosome.nvim.io.state import NS

from proteome.components.core.tpe import CoreRibosome
from proteome.persistence.buffers import persist_buffers


@prog
@do(NS[CoreRibosome, None])
def save() -> Do:
    yield NS.lift(persist_buffers())


__all__ = ('save',)
