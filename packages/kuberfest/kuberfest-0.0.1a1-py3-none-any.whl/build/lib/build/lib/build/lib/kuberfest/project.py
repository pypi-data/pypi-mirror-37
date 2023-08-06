from kuberfest.consts import kuberfest_dir
from kuberfest.tools.debug import Debug
import sys
import os


class Project:
    def __init__(self, project_dir):
        self.dir = project_dir
        self._is_development = False
        self.settings = self.get_project_settings()
        self.variables = self.get_project_variables() 

    def get_project_settings(self):
        try:
            project_dir = "{0}/{1}".format(self.dir, kuberfest_dir)
            Debug.info("Importing project settings at '{}'...".format(project_dir))
            sys.path.append(project_dir)
            import settings as project_settings
            return project_settings

        except ModuleNotFoundError:
            Debug.info("Project dir not found at '{}'".format(project_dir))

    def delete_tmp_dir(self):
        os.system('rm -r {0}/{1}'.format(self.dir, self.settings.output_dir))
        os.system('mkdir {0}/{1}'.format(self.dir, self.settings.output_dir))
    
    def set_development(self, is_development):
        self._is_development = is_development

    def is_development(self):
        return self._is_development

    def get_project_variables(self):
        try:
            # TODO: Find a way to parse the variables file with parameters
            import variables
            return variables.__dict__
        except ModuleNotFoundError:
            Debug.info("You must have a 'variables.py' file in your project's 'kuberfest' folder")
            exit()

    def get_variable(self, variable_name):
        variables = self.get_project_variables()
        if variable_name not in variables:
            debug("Variable '{}' not found".format(variable_name))
            exit()

        return variables[variable_name]
