import os
from kuberfest.tools.kubernetes import KubernetesTool


def run(project, value):
    if not value:
        return True

    kubernetes_tool = KubernetesTool(project)
    
    function_unavailable_error = "--init-db command requires a 'functions.py' module with an 'init_db(namespace, db_pod)' function"
    try:
        import functions as project_functions
        if not hasattr(project_functions, 'init_db') or not callable(project_functions.init_db):
            debug(function_unavailable_error)

            return False
        else:
            db_pod = kubernetes_tool.get_pods(
                namespace=tools.get_variable('NAMESPACE'), 
                app_name=tools.get_variable('DB_APP_NAME')[0]
            )
            project_functions.init_db(
                project=project,
                namespace=tools.get_variable('NAMESPACE'),
                db_pod=db_pod
            )

            return True
    except ImportError as e:
        debug(function_unavailable_error)
        
        return False
