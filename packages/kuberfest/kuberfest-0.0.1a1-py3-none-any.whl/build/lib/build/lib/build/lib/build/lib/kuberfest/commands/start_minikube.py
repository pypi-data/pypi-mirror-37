import os

def run(project, value):
    if not value:
        return True
        
    # if os.popen('minikube ip').read().strip() == '':
    os.system('minikube start')

    return True