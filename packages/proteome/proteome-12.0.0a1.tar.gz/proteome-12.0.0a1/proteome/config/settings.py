import json
from typing import Any

from ribosome.config.setting import str_setting, path_list_setting, setting_ctor, json_setting, path_setting

from amino import Right, Nil, Either, Dat, Path, Maybe, List, Lists, do, Do, Map
from amino.json.decoder import decode_json_type

from proteome.data.project import Project, DirProject


class ProjectSpec(Dat['ProjectSpec']):

    def __init__(
            self,
            name: str,
            root: Path,
            type: Maybe[str],
            types: Maybe[List[str]],
            lang: Maybe[str],
            langs: Maybe[List[str]],
    ) -> None:
        self.name = name
        self.type = type
        self.types = types
        self.lang = lang
        self.langs = langs


@do(Either[str, Project])
def cons_project(data: Any) -> Do:
    js = yield json.dumps(data)
    spec = yield decode_json_type(js, ProjectSpec)
    return Project(DirProject(spec.name, spec.root, spec.type), spec.types, spec.lang, spec.langs)


def cons_projects(data: list) -> Either[str, List[Project]]:
    return Lists.wrap(data).traverse(cons_project, Either)


class ProjectConfig(Dat['ProjectConfig']):

    @staticmethod
    def cons(
            types: Map[str, List[str]],
    ) -> 'ProjectConfig':
        return ProjectConfig(
            types,
        )

    def __init__(self, types: Map[str, List[str]]) -> None:
        self.types = types


projects_setting = setting_ctor(list, cons_projects)
project_config_setting = json_setting(ProjectConfig)

main_project_dir_help = '''Override the location of the main project, which usually is the current working directory.
'''
main_name_help = '''Contains the name of the main project after startup, intended as read-only.
'''
main_type_help = '''Contains the type of the main project after startup, intended as read-only.
'''

main_project_metadata = str_setting('main_project_metadata', 'main_project metadata resolver', '', True)
main_project_dir = path_setting('main_project_dir', 'location of the main project', main_project_dir_help, True)
projects = projects_setting('projects', 'special projects', '', True, Right(Nil))
project_type_dirs = path_list_setting('project_type_dirs', 'base dirs for project types', '', True, Right(Nil))
project_config = project_config_setting('project_config', 'global project configuration', '', True)
main_name = str_setting('main_name', 'name of the main project', main_name_help, True)
main_type = str_setting('main_type', 'type of the main project', main_type_help, True)

__all__ = ('main_project_metadata', 'main_project_dir', 'projects', 'project_type_dirs', 'project_config', 'main_name',
           'main_type',)
