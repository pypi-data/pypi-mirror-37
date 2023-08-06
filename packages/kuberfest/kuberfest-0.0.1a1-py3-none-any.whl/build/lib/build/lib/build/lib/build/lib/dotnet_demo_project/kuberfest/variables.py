# Kubernetes context
CONTEXT='minikube'

# Docker hub
REPOSITORY='kuberfest/dotnet-demo-project'

# Namespace
NAMESPACE='kuberfest-dotnet-demo-project'

# API
API_NAME='api'
API_DEPLOYMENT_NAME='{0}-deployment'.format(API_NAME)
API_DEPLOYMENT_REPLICAS=3
API_APP_NAME='{0}-app'.format(API_NAME)
API_CONTAINER_NAME='{0}-container'.format(API_NAME)
# API_ASPNETCORE_ENVIRONMENT='Development' if project.is_development() else 'Production'
# TODO: This
API_ASPNETCORE_ENVIRONMENT='Development'

API_SERVICE_NAME='{0}-service'.format(API_NAME)
API_SERVICE_PORT=80
API_SERVICE_TARGET_PORT=API_SERVICE_PORT
API_SERVICE_NODE_PORT=30080

# DB
DB_NAME='db'
DB_DEPLOYMENT_NAME='{0}-deployment'.format(DB_NAME)
DB_APP_NAME='{0}-app'.format(DB_NAME)
DB_SERVICE_NAME='{0}-service'.format(DB_APP_NAME)
DB_SERVER=DB_SERVICE_NAME
DB_PORT='5432'
DB_PORT_NAME='{0}-port'.format(DB_APP_NAME)
DB_USERNAME='postgres'
DB_PASSWORD='123'
DB_DATABASE='service'

# Storage
DB_STORAGE_NAME='{0}-storage'.format(DB_APP_NAME)
DB_STORAGE_SIZE='300M'
DB_PV_CLAIM_NAME='{0}-pv-claim'.format(DB_APP_NAME)

DB_CONNECTION_STRING="postgresql://{username}:{password}@localhost:{port}".format(
        username=DB_USERNAME,
        password=DB_PASSWORD,
        server=DB_SERVICE_NAME,
        port=DB_PORT,
    )