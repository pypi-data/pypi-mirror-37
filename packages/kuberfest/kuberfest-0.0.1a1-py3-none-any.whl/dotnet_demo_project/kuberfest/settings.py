kuberfest_dir = "./kuberfest"
templates_dir = "{0}/templates".format(kuberfest_dir)
output_dir = "{0}/output".format(kuberfest_dir)
output_yaml_file_name = 'output.yaml'
template_file_names = [
    "namespace.yaml",
    "db-service.yaml",  
    "db-deployment.yaml",
    "db-pv-claim.yaml",
    "api-service.yaml",
    "api-deployment.yaml",
]