from kuberfest.tools.debug import Debug

def run(project, value):
    if not value:
        return True

    Debug.info(
        "Starting deployment with {0} environment...".format(
            'DEVELOPMENT' if project.is_development() else 'PRODUCTION'
        )
    )

    return True