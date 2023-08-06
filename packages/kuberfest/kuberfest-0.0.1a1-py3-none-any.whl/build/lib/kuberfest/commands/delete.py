from kuberfest.tools.kubernetes import KubernetesTool
from kuberfest.tools.debug import Debug


def run(project, value):
    if not value:
        return True

    kubernetes_tool = KubernetesTool(project)

    key_input = input(
        "Are you sure you want to delete the namespace '{0}'? y/n\n".format(
            project.get_variable('NAMESPACE')
        )
    )
    while(True):
        if key_input.lower() == 'y':
            kubernetes_tool.delete_namespace(project.get_variable('NAMESPACE'))
            return True
        elif key_input.lower() == 'n':
            Debug.error("Cancelling...")
            return False
        else:
            key_input = input("Please input 'y' or 'n'\n")
