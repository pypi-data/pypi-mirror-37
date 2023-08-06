import os
from kuberfest.tools.debug import Debug


def run(project, value):
    if not value:
        return True

    Debug.info("Building container...")
    repository = project.get_variable('REPOSITORY')
    cwd = os.getcwd()
    os.chdir(project.dir)
    os.system(
        'docker-compose build'.format(repository)
    )
    os.chdir(cwd)

    return True