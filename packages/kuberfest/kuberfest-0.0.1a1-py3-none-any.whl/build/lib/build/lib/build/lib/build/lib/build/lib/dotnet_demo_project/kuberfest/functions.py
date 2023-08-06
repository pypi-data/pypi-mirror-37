import os
from tools import get_variables, debug, get_project_dir
from settings import kuberfest_dir


def wait_for_db(project, namespace, db_pod):
    debug("Waiting for postgres at: ... {0}".format(project.get_variable('DB_CONNECTION_STRING')))
    while (True):
        result=os.popen(
            'kubectl exec -it --namespace={namespace} {pod} -- psql {connection_string} -c "\q"'.format(
                namespace=namespace,
                pod=db_pod,
                connection_string=project.get_variable('DB_CONNECTION_STRING'),
            )
        ).read()

        if 'could not connect to server' not in result:
            break

def create_db(project, namespace, db_pod, database):
    debug("Creating Database...")
    os.system(
        'kubectl exec -it --namespace={namespace} {pod} -- psql {connection_string} -c "CREATE DATABASE {database};"'.format(
            namespace=namespace,
            pod=db_pod,
            connection_string=project.get_variable('DB_CONNECTION_STRING'),
            database=database,
        )
    )

def init_schema(project, namespace, db_pod, sql_init_file_path):
    debug("Copying migration file to the pod...")
    sql_init_file_name = sql_init_file_path.split("/")[-1]
    os.system(
        'kubectl cp {sql_init_file_path} {namespace}/{pod}:/{sql_init_file_name}'.format(
            namespace=namespace,
            pod=db_pod,
            sql_init_file_path=sql_init_file_path,
            sql_init_file_name=sql_init_file_name,
        ) 
    )

    debug("Importing SQL from inside the pod to the DB...")
    os.system(
        'kubectl exec -it --namespace={namespace} {pod} -- psql {connection_string}/{database} -f /{sql_init_file_name}'.format(
            namespace=namespace,
            pod=db_pod,
            connection_string=project.get_variable('DB_CONNECTION_STRING'),
            sql_init_file_name=sql_init_file_name,
            database=get_variable('DB_DATABASE'),
        )
    )

def init_db(project, namespace, db_pod):
    wait_for_db(
        namespace=namespace, 
        db_pod=db_pod
    )
    create_db(
        project=project,
        namespace=namespace,
        db_pod=db_pod, 
        database=project.get_variable('DB_DATABASE')
    )
    init_schema(
        project=project,
        namespace=namespace, 
        db_pod=db_pod,
        sql_init_file_path="{0}/{1}/init.sql".format(project.dir, kuberfest_dir)
    )
