from amino import do, Do, Maybe
from amino.case import Case

from ribosome.nvim.io.compute import NvimIO
from ribosome.nvim.api.command import runtime
from ribosome.nvim.io.api import N

from proteome.data.project import Project, DirProject, VirtualProject, ProjectMetadata


def runtime_conf(conf_dir: str, path: str) -> NvimIO[None]:
    return runtime(f'{conf_dir}/{path}')


@do(NvimIO[None])
def type_project_conf(conf_dir: str, tpe: str, name: str) -> Do:
    yield runtime_conf(conf_dir, tpe)
    yield runtime_conf(conf_dir, f'{tpe}/{name}')


class read_config_config_meta(Case[ProjectMetadata, NvimIO[None]], alg=ProjectMetadata):

    def __init__(self, conf_dir: str, project: Project) -> None:
        self.conf_dir = conf_dir
        self.project = project

    @do(NvimIO[None])
    def dir(self, meta: DirProject) -> Do:
        yield meta.tpe.traverse(lambda a: type_project_conf(self.conf_dir, a, meta.name), NvimIO)

    def virtual(self, a: VirtualProject) -> NvimIO[None]:
        return N.unit


@do(NvimIO[None])
def read_config_project(conf_dir: str, project: Project) -> Do:
    yield read_config_config_meta(conf_dir, project)(project.meta)
    yield project.types.traverse(lambda a: runtime_conf(conf_dir, a), NvimIO)


@do(NvimIO[None])
def read_config(conf_dir: str, project: Maybe[Project]) -> Do:
    yield runtime_conf(conf_dir, 'all/*')
    yield project.traverse(lambda a: read_config_project(conf_dir, a), NvimIO)


__all__ = ('read_config_config', 'read_config',)
