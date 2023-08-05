import os

from onepanel.utilities.connection import Connection
from onepanel.commands.datasets import DatasetViewController
from onepanel.commands.projects import ProjectViewController


class PrePushToEndpointHook:

    version = None

    def __init__(self):
        self.version = "1.0.0"


    @staticmethod
    def ping_endpoint():
        conn = Connection()
        conn.load_credentials()
        data = {
            'version':'1',
            'data':''
        }

        # Figure out if this is a project or dataset push
        home = os.getcwd()
        onepanel_dir = os.path.join(home, '.onepanel')
        if not os.path.exists(onepanel_dir):
            print("ERROR.Directory does not exist, cannot connect to endpoint.")
            print("DETAILS." + onepanel_dir)
            exit(-1)
        dataset_file = os.path.join(home, DatasetViewController.DATASET_FILE)
        dataset_push = True
        if not os.path.isfile(dataset_file):
            dataset_push = False
        else:
            # Safe to ping the endpoint with dataset credentials
            dvc = DatasetViewController(conn)
            dvc.init_credentials_retrieval()
            url_params = '/gitlab/accounts/{account_uid}/project/{project_uid}/update'.format(
                account_uid=dvc.account_uid, project_uid=dvc.dataset_uid
            )
            try:
                dvc.post(data,params=url_params)
            except ValueError as e:
                print("Gitlab Update Failed.")

        project_push = True
        project_file = os.path.join(home, ProjectViewController.PROJECT_FILE)
        if not os.path.isfile(project_file):
            project_push = False
        else:
            # Safe to ping the endpoint with project credentials
            pvc = ProjectViewController(conn)
            pvc.init_credentials_retrieval()
            url_params = '/gitlab/accounts/{account_uid}/project/{project_uid}/update'.format(
                account_uid=pvc.account_uid,project_uid=pvc.project_uid
            )
            try:
                pvc.post(data,params=url_params)
            except ValueError as e:
                print("Gitlab Update Failed.")

        if project_push == False and dataset_push == False:
            print("ERROR. Cannot connect to endpoint, unclear if this code is initialized with 'onepanel init'.")
            exit(-1)
