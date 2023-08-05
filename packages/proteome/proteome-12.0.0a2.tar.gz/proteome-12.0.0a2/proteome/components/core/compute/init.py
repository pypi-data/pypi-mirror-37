from typing import Tuple, Callable

from amino import do, Do, Path, IO, Either, Just, Maybe, List, Map
from amino.case import Case

from proteome.components.core.tpe import CoreRibosome
from proteome.config.settings import (main_project_metadata, project_type_dirs, projects, project_config,
                                      main_project_dir, ProjectSpec, ProjectConfig, main_name, main_type)
from proteome.data.project import DirProject, Project, ProjectMetadata, VirtualProject
from proteome.components.core.data.core_data import CoreData
from proteome.persistence.buffers import load_persisted_buffers

from ribosome.compute.api import prog
from ribosome.nvim.io.state import NS
from ribosome.compute.ribosome_api import Ribo
from ribosome.compute.prog import Prog
from ribosome.nvim.io.compute import NvimIO
from ribosome.nvim.io.api import N


@do(IO[Tuple[Path, str, str]])
def path_data(override: Either[str, Path]) -> Do:
    cwd = yield override.cata(lambda e: IO.delay(Path.cwd), IO.pure)
    return cwd, cwd.name, cwd.parent.name


def resolve_project(
        type_dirs: Map[str, Path],
        explicit: List[ProjectSpec],
        config: ProjectConfig,
) -> Callable[[Path, str, Maybe[str]], Project]:
    def resolve_project(root: Path, name: str, tpe: Maybe[str]) -> Project:
        by_path = explicit.find(lambda a: a.root == root)
        by_type_name = tpe.flat_map(lambda t: explicit.find(lambda a: a.name == name and a.type.contains(t)))
        return by_path.o(by_type_name).get_or(lambda: Project.cons(DirProject(name, root, tpe)))
    return resolve_project


@prog
@do(NS[CoreRibosome, Project])
def builtin_project_metadata() -> Do:
    main_dir = yield Ribo.setting_e(main_project_dir)
    root, name, tpe = yield NS.from_io(path_data(main_dir))
    type_dirs = yield Ribo.setting(project_type_dirs)
    explicit = yield Ribo.setting(projects)
    config = yield Ribo.setting_e(project_config)
    return resolve_project(type_dirs, explicit, config)(root, name, Just(tpe))


@prog.do(Project)
def main_project() -> Do:
    custom = yield Ribo.setting_prog_e(main_project_metadata)
    handler = yield custom.cata(lambda e: Prog.pure(builtin_project_metadata), lambda c: Prog.e(Either.import_path(c)))
    yield handler()


class set_project_vars(Case[ProjectMetadata, NvimIO[None]], alg=ProjectMetadata):

    @do(NvimIO[None])
    def dir(self, a: DirProject) -> Do:
        yield main_name.update(a.name)
        yield a.tpe.traverse(main_type.update, NvimIO)

    def virtual(self, a: VirtualProject) -> NvimIO[None]:
        return N.unit


@prog
@do(NS[CoreRibosome, None])
def init_with_main(main: Project) -> Do:
    yield Ribo.modify_main(lambda s: s.set.main(Just(main)))
    yield NS.lift(set_project_vars.match(main.meta))
    yield NS.lift(load_persisted_buffers())


@prog.do(type(None))
def init() -> Do:
    main = yield main_project()
    yield init_with_main(main)


__all__ = ('init',)
