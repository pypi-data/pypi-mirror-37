import os
import settings
from kuberfest.tools.debug import Debug


def run(project, value):
    if not value:
        return True

    Debug.info("Pushing docker file...")
    cwd = os.getcwd()
    os.chdir(project.dir)
    os.system(
        'docker push {}'.format(
            project.get_variable('REPOSITORY')
        )
    )
    os.chdir(cwd)

    return True