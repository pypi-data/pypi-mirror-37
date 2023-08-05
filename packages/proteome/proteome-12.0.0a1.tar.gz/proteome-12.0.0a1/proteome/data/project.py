from amino import Dat, Path, Maybe, Nil, List, ADT


class ProjectMetadata(ADT['ProjectMetadata']):
    pass


class DirProject(ProjectMetadata):

    @staticmethod
    def cons(
            name: str,
            root: Path,
            tpe: str=None,
    ) -> 'DirProject':
        return DirProject(
            name,
            root,
            Maybe.optional(tpe),
        )

    def __init__(self, name: str, root: Path, tpe: Maybe[str]) -> None:
        self.name = name
        self.root = root
        self.tpe = tpe


class VirtualProject(ProjectMetadata):

    def __init__(self, name: str) -> None:
        self.name = name


class Project(Dat['Project']):

    @staticmethod
    def cons(
            meta: ProjectMetadata,
            types: List[str]=Nil,
            lang: str=None,
            langs: List[str]=Nil,
    ) -> 'Project':
        return Project(
            meta,
            types,
            Maybe.optional(lang),
            langs,
        )

    def __init__(
            self,
            meta: ProjectMetadata,
            types: List[str],
            lang: Maybe[str],
            langs: List[str],
    ) -> None:
        self.meta = meta
        self.types = types
        self.lang = lang
        self.langs = langs


__all__ = ('Project', 'ProjectMetadata', 'DirProject', 'VirtualProject',)
