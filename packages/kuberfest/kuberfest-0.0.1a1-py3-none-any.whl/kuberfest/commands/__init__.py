import importlib
import argparse
from kuberfest import consts
from kuberfest.tools.debug import Debug
from kuberfest.consts import kuberfest_dir
import sys


# Commands will be run in the same order of the dictionary
commands = {
    'development': {
        'short': 'dev',
        'description': 'run as a development environment.',
        'const': False,
        'default': False,
        'action': 'store',
        'type': bool,
        'nargs': '?',
    },
    'print_environment': {
        'short': 'env',
        'description': 'print the deployment environment.',
        'const': True,
        'default': True,
        'hidden': True,
        'action': 'store',
        'type': bool,
        'nargs': '?',
    },
    'context': {
        'short': 'ctx',
        'description': 'switch Kubernetes context',
        'default': 'minikube',
        'action': 'store',
        'type': str,
        'nargs': '?',
    },
    'delete': {
        'short': 'del',
        'description': 'delete the kubernetes namespace.',
        'const': True,
        'default': False,
        'action': 'store',
        'type': bool,
        'nargs': '?',
    },
    'start_minikube': {
        'short': 'smk',
        'description': 'start minikube as part of the deployment.',
        'const': True,
        'default': False,
        'action': 'store',
        'type': bool,
        'nargs': '?',
    },
    'build': {
        'short': 'bld',
        'description': 'build the project and container.',
        'const': True,
        'default': False,
        'action': 'store',
        'type': bool,
        'nargs': '?',
    },
    'push': {
        'short': 'psh',
        'description': 'push the docker to the repository.',
        'const': True,
        'default': False,
        'action': 'store',
        'type': bool,
        'nargs': '?',
    },
    'deploy': {
        'short': 'dep',
        'description': 'deploy kubernetes yamls.',
        'const': True,
        'default': False,
        'action': 'store',
        'type': bool,
        'nargs': '?',
    },
    'minikube_ip': {
        'short': 'mkip',
        'description': 'print minikube ip.',
        'const': True,
        'default': True,
        'hidden': True,
        'action': 'store',
        'type': bool,
        'nargs': '?',
    }
}


class CommandsController:
    parsed_arguments = None
    project_dir_argument = 'project_dir'

    def __init__(self, project):
        self.project = project

    def get_all_commands(self):
        project_commands = self.get_project_commands()
        if project_commands is None:
            return commands

        return {**commands, **project_commands.commands}

    def get_project_commands(self):
        if self.project is None:
            return None

        try:
            project_dir = "{0}/{1}".format(self.project.dir, kuberfest_dir)
            Debug.info("Importing project commands at '{}'...".format(project_dir))
            sys.path.append(project_dir)
            import commands as project_commands
            return project_commands

        except ModuleNotFoundError:
            Debug.info("Project dir not found at '{}'".format(project_dir))

    @staticmethod
    def get_project_dir_from_arguments():
        parser = argparse.ArgumentParser(
            prog=consts.kuberfest_name,
            description=consts.kuberfest_description,
            add_help=False,
        )

        # Project dir argument
        parser.add_argument(
            CommandsController.project_dir_argument,
            nargs='?',
            action='store',
            help='Project app directory',
        )

        project_dirs = parser.parse_known_args()[0].__dict__[CommandsController.project_dir_argument]

        if project_dirs is None:
            return None

        return project_dirs

    def parse_arguments(self):
        if CommandsController.parsed_arguments is not None:
            return CommandsController.parsed_arguments

        parser = argparse.ArgumentParser(
            prog=consts.kuberfest_name,
            description=consts.kuberfest_description,
            add_help=True,
        )

        # Project dir argument
        parser.add_argument(
            CommandsController.project_dir_argument,
            nargs=1,
            action='store',
            help='Project app directory',
        )

        # Commands arguments
        for command, command_data in self.get_all_commands().items():
            parser.add_argument(                
                '--{}'.format(command),
                '--{}'.format(command_data['short']),
                metavar=str(command_data['type'])[8:-2],
                nargs=command_data['nargs'],
                action=command_data['action'],
                # Uses this vlaue if arg appears, but no explicit value is given 
                const=command_data['const'] if 'const' in command_data else None,
                # Uses this value if arg doesn't appear
                default=command_data['default'] if 'default' in command_data else None, 
                required=True if 'default' not in command_data else None,
                type=command_data['type'],
                help=argparse.SUPPRESS if 'hidden' in command_data and command_data['hidden'] else command_data['description'],
            )

        CommandsController.parsed_arguments = parser.parse_args().__dict__
        return CommandsController.parsed_arguments

    def _run_command(self, command, values, module_base):
        i = importlib.import_module('{}.{}'.format(module_base, command))
        result = i.run(self.project, values)
        if not result:
            return False

        return True

    def run_commands(self):
        parsed_arguments = self.parse_arguments()

        if self.project is None:
            return

        Debug.info("Running Kuberfest commands...")
        for command in commands.keys():
            if not self._run_command(command, parsed_arguments[command], 'kuberfest.commands'):
                Debug.error('Stopped with partial results.')
                return

        Debug.info("Running project commands...")
        for command in self.get_project_commands().commands.keys():
            if not self._run_command(command, parsed_arguments[command], 'commands'):
                Debug.error('Stopped with partial results.')
                return
