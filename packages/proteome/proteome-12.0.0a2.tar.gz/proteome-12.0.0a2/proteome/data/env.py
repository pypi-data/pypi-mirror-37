from amino import List, Dat, Nil, Maybe

from proteome.data.project import Project


class Env(Dat['Env']):

    @staticmethod
    def cons(
            projects: List[Project]=Nil,
            main: Project=None,
    ) -> 'Env':
        return Env(
            projects,
            Maybe.optional(main)
        )

    def __init__(self, projects: List[Project], main: Maybe[Project]) -> None:
        self.projects = projects
        self.main = main


__all__ = ('Env',)
