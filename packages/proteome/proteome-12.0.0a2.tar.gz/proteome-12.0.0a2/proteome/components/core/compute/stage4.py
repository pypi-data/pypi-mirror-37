from amino import do, Do

from ribosome.compute.api import prog
from ribosome.nvim.io.state import NS
from ribosome.compute.ribosome_api import Ribo

from proteome.components.core.tpe import CoreRibosome
from proteome.project.config import read_config


@prog
@do(NS[CoreRibosome, None])
def stage4() -> Do:
    main = yield Ribo.inspect_main(lambda a: a.main.to_maybe)
    yield NS.lift(read_config('after/project', main))


__all__ = ('stage4',)
