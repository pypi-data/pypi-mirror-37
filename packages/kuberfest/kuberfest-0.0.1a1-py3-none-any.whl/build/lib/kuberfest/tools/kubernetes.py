from kuberfest.tools.base import BaseTool
import os
from kuberfest.tools.debug import Debug


class KubernetesTool(BaseTool):
    '''
    Tool for various Kubernetes activities.
    '''

    def switch_config(self, config_name):
        os.system(
            'kubectl config use-context {context}'.format(
                context=config_name
            )
        )

    def wait_for_deployments(self, namespace, deployments):
        Debug.info("Waiting for deployments... [{}]".format(', '.join(deployments)))
        while (True):
            successes=0
            for deployment in deployments:
                status=os.popen(
                    'kubectl rollout status deploy/{deployment} --namespace={namespace}'.format(
                        namespace=namespace,
                        deployment=deployment,
                    )
                ).read().strip()

                print(status)
                
                # TODO: This is currently not working, find a way to read this line
                if 'error: deployment "{}" exceeded its progress deadline'.format(deployment) in status:
                    # TODO: Possible fallback here
                    Debug.error('Something went wrong with Kubernetes.')
                    return False

                if 'deployment "{}" successfully rolled out'.format(deployment) in status:
                    Debug.info(status)
                    successes += 1

            if successes == len(deployments):
                break

        return True

    def get_pods(self, namespace, app_name):
        pods_string = os.popen(
            'kubectl get pods --namespace={namespace} -l app={app_name} -o=jsonpath=\'{{range .items[*]}}{{.metadata.name}},{{end}}\''.format(
                namespace=namespace,
                app_name=app_name,
            )).read()

        pods_string = pods_string[:len(pods_string)-1]
        return pods_string.split(',')

    def delete_namespace(self, namespace):
        os.system(
            'kubectl delete namespaces {namespace}'.format(
                namespace=namespace
            )
        )

    def run_yaml(self, yaml_file_name, **kwargs):
        '''
        Apply a yaml file on Kubernetes.
        '''
        os.system(
            'kubectl apply -f {project_dir}/{output_dir}/{yaml_file_name}'.format(
                project_dir=self.project.dir,
                output_dir=self.project.settings.output_dir,
                yaml_file_name=yaml_file_name,
            )
        )
