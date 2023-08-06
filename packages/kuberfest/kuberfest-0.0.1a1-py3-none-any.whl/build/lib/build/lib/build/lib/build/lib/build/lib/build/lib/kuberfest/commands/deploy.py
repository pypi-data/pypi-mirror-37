from kuberfest.tools.kubernetes import KubernetesTool
import os
import settings
from kuberfest.tools.kubernetes_yaml import KubernetesYamlTool
from kuberfest.tools.debug import Debug


def run(project, value):
    if not value:
        return True

    Debug.info("Setting up kubernetes yamls...")

    yaml_tool = KubernetesYamlTool(project)
    kubernetes_tool = KubernetesTool(project)

    project.delete_tmp_dir()
    yamls = list()
    for yaml_file_name in settings.template_file_names:
        yamls.append(yaml_tool.get_yaml(yaml_file_name, **project.variables))
    yaml_tool.merge_yamls(yamls, settings.output_yaml_file_name)

    Debug.info("Deploying generated yamls to Kubernetes...")
    kubernetes_tool.run_yaml(settings.output_yaml_file_name)
    deployments = list()
    deployments_data = yaml_tool.get_yaml_types(yaml_tool.get_output_yaml(), 'Deployment')
    for deployment_data in deployments_data:
        deployments.append(deployment_data['metadata']['name'])

    return kubernetes_tool.wait_for_deployments(
        namespace=project.get_variable('NAMESPACE'),
        deployments=deployments,
    )

    return True
