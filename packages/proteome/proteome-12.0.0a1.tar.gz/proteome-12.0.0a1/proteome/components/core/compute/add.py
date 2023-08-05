from amino import do, Do, Dat, Maybe, Path, List, Nil

from proteome.components.core.tpe import CoreRibosome
from proteome.data.project import Project, DirProject, VirtualProject

from ribosome.compute.api import prog
from ribosome.nvim.io.state import NS
from ribosome.compute.ribosome_api import Ribo


class AddOptions(Dat['AddOptions']):

    def __init__(
            self,
            root: Maybe[Path],
            type: Maybe[str],
            types: Maybe[List[str]],
            lang: Maybe[str],
            langs: Maybe[List[str]],
    ) -> None:
        self.root = root
        self.type = type
        self.types = types
        self.lang = lang
        self.langs = langs


@prog
@do(NS[CoreRibosome, None])
def add(name: str, options: AddOptions) -> Do:
    meta = options.root.map(lambda a: DirProject(name, a, options.type)).get_or(VirtualProject, name)
    project = Project(meta, options.types.get_or_strict(Nil), options.lang, options.langs.get_or_strict(Nil))
    yield Ribo.modify_main(lambda s: s.append1.projects(project))


__all__ = ('add',)
