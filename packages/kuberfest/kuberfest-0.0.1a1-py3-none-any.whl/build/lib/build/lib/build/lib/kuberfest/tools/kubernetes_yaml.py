from kuberfest.tools.base import BaseTool
import os
import yaml as yaml_module


class KubernetesYamlTool(BaseTool):
    '''
    Tool for reading, manipulating and parsing Kubernetes related yaml files.
    '''

    def get_yaml(self, yaml_file_name, **kwargs):
        with open(
            "{project_dir}/{templates_dir}/{yaml_file_name}".format(
                project_dir=self.project.dir,
                templates_dir=self.project.settings.templates_dir,
                yaml_file_name=yaml_file_name,
            ), 'r') as yaml_file:
            yaml_string = yaml_file.read()
            return yaml_string.format(**kwargs)

    def merge_yamls(self, yamls_list, output_file_name):
        all_yaml_strings = ''
        for yaml_string in yamls_list:
            all_yaml_strings += '---\n{0}\n\n'.format(yaml_string.strip())
            
        with open(
            "{project_dir}/{output_dir}/{output_file_name}".format(
                project_dir=self.project.dir,
                output_dir=self.project.settings.output_dir, 
                output_file_name=output_file_name
            ),
            "w+"
        ) as yaml_file:
            yaml_file.write(all_yaml_strings)

    def get_yaml_types(self, yaml_string, yaml_type):
        ret_list = list()
        
        yamls = yaml_string.split('---')
        for yaml in yamls:
            if len(yaml.strip()) > 0:
                yaml_dict = yaml_module.load(yaml)
                if isinstance(yaml_dict, dict) and yaml_dict['kind'] == yaml_type:               
                    ret_list.append(yaml_dict)

        return ret_list

    def get_output_yaml(self):
        with open(
            '{}/{}/{}'.format(
                self.project.dir, 
                self.project.settings.output_dir, 
                self.project.settings.output_yaml_file_name
            ), 
            'r'
        ) as output_yaml_file:
            yaml_string = output_yaml_file.read()
            return yaml_string