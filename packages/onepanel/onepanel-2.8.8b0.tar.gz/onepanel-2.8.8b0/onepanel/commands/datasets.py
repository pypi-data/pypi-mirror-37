""" Command line interface for the OnePanel Machine Learning platform

'Datasets' commands group.
"""
import glob
import os
import re

import click
import configobj
import humanize

from onepanel.commands.base import APIViewController
from onepanel.commands.login import login_required
from onepanel.utilities.aws_utility import AWSUtility
from onepanel.utilities.s3_authenticator import S3Authenticator


class DatasetViewController(APIViewController):
    """ DatasetViewController data model
    """

    DATASET_FILE = os.path.join('.onepanel','dataset')
    EXCLUSIONS = [os.path.join('.onepanel','dataset')]

    account_uid = None
    dataset_uid = None

    def __init__(self, conn):
        APIViewController.__init__(self, conn)
        self.endpoint = '{}'.format(
            self.conn.URL,
        )

    def init_credentials_retrieval(self):
        # Figure out the account uid and dataset uid
        home = os.getcwd()
        onepanel_dir = os.path.join(home, '.onepanel')
        if not os.path.exists(onepanel_dir):
            print("ERROR.Directory does not exist, cannot carry out all datasets operations.")
            print("DETAILS." + onepanel_dir)
            exit(-1)
        dataset_file = os.path.join(home, DatasetViewController.DATASET_FILE)
        if not os.path.isfile(dataset_file):
            print("ERROR.Dataset file does not exist, cannot carry out all datasets operations.")
            print("DETAILS." + dataset_file)
            exit(-1)

        cfg = configobj.ConfigObj(dataset_file)

        dataset_uid = cfg['uid']
        dataset_account_uid = cfg['account_uid']

        if len(dataset_uid) < 1 or len(dataset_account_uid) < 1:
            print("ERROR.Dataset file has invalid credentials. Verify credentials or re-pull project.")
            exit(-1)
        self.account_uid = dataset_account_uid
        self.dataset_uid = dataset_uid


    def save(self, home):
        if not os.path.exists(home):
            os.makedirs(home)
        onepanel_dir = os.path.join(home, '.onepanel')
        if not os.path.exists(onepanel_dir):
            os.makedirs(onepanel_dir)
        dataset_file = os.path.join(home, DatasetViewController.DATASET_FILE)

        cfg = configobj.ConfigObj(dataset_file)
        cfg['uid'] = self.dataset_uid
        cfg['account_uid'] = self.account_uid
        cfg.write()

    def init_endpoint(self):
        self.endpoint = '{root}/accounts/{account_uid}/datasets/{dataset_uid}'.format(
            root=self.conn.URL,
            account_uid=self.account_uid,
            dataset_uid=self.dataset_uid
        )

    @classmethod
    def from_json(cls, data):
        cls.account_uid = data['account']['uid']
        cls.dataset_uid = data['uid']

    @classmethod
    def is_uid_valid(cls,uid):
        pattern = re.compile('^[a-z0-9][-a-z0-9]{1,23}[a-z0-9]$')
        if pattern.match(uid):
            return True
        else:
            return False

    @classmethod
    def exists_local(cls,home):
        dataset_file = os.path.join(home, DatasetViewController.DATASET_FILE)
        if os.path.isfile(dataset_file):
            return True
        else:
            return False

    @classmethod
    def exists_remote(cls,dataset_uid, data):
        exists = False
        if data['uid'] == dataset_uid:
            exists = True
        return exists


def create_dataset(ctx, account_uid, home):
    """ Dataset creation method for 'datasets_init' and 'datasets_create'
    commands
    """
    vc = ctx.obj['vc']

    if not account_uid:
        account_uid = ctx.obj['connection'].account_uid

    dataset_uid = os.path.basename(home)
    if not vc.is_uid_valid(dataset_uid):
        click.echo('Dataset name {} is invalid.'.format(dataset_uid))
        click.echo(
            'Name should be 3 to 25 characters long, lower case alphanumeric or \'-\' and must start and end with an alphanumeric character.')
        return None

    # Check if the dataset already exists remotely
    url_dataset_check = '/accounts/{}/datasets/{}'.format(account_uid, dataset_uid)
    response_data = vc.get(params=url_dataset_check)
    remote_dataset = response_data['data']

    dataset = None
    # If remote returned data, do operations
    if remote_dataset is not None and vc.exists_remote(dataset_uid, remote_dataset):
        click.echo("Dataset already exists. Please download the dataset if you want to use it.")
        return None
    # If no data from remote, we can create a dataset
    else:
        can_create = True
        if vc.exists_local(home):
            can_create = click.confirm(
                'Dataset exists locally but does not exist in {}, create the dataset and remap local folder?'
                    .format(account_uid))

        if can_create:
            data = {
                'uid': dataset_uid
            }
            url_dataset_create = '/accounts/{}/datasets'.format(account_uid)
            response = vc.post(data,params=url_dataset_create)
            if response['status_code'] == 200:
                vc.from_json(response['data'])
                vc.save(home)
            else:
                click.echo("Encountered error.")
                click.echo(response['status_code'])
                click.echo(response['data'])
                return False
    return True


@click.group(help='Dataset commands group')
@click.pass_context
def datasets(ctx):
    ctx.obj['vc'] = DatasetViewController(ctx.obj['connection'])


@datasets.command('list', help='Display a list of all datasets.')
@click.pass_context
@login_required
def datasets_list(ctx):
    vc = ctx.obj['vc']
    data = vc.list(params='/datasets')
    if data is None or len(data['data']) < 1:
        print("No datasets found.")
    else:
        data_print = []
        for datum in data['data']:
            uid = datum['uid']
            version_count = datum['statistics']['version']
            statistics_data = datum['statistics']['data']
            size = 0
            if len(statistics_data) > 0:
                size = datum['statistics']['data']['storage_size']
            size_formatted = humanize.naturalsize(size, binary=True)
            data_print.append({'uid': uid,
                               'version_count': version_count,
                               'size': size_formatted
                               })

        empty_message = "No datasets found."
        fields = ['uid', 'version_count', 'size']
        field_names = ['NAME', 'VERSIONS', 'SIZE']
        DatasetViewController.print_items(data_print, fields, field_names, empty_message)


@datasets.command('init', help='Initialize dataset in current directory.')
@click.pass_context
@login_required
def datasets_init(ctx):
    vc = ctx.obj['vc']
    home = os.getcwd()
    if not vc.is_uid_valid(os.path.basename(home)):
        dataset_uid = click.prompt('Please enter a valid dataset name')
        home = os.path.join(home, dataset_uid)

    if create_dataset(ctx, None, home):
        click.echo('Dataset is initialized in current directory.')


@datasets.command('create', help='Create dataset in new directory.')
@click.argument('name', type=str)
@click.pass_context
@login_required
def datasets_create(ctx, name):
    home = os.path.join(os.getcwd(), name)
    if create_dataset(ctx, None, home):
        click.echo('Dataset is created in directory {}.'.format(home))

@datasets.command('push', help='Push up dataset changes')
@click.option(
    '-m', '--message',
    type=str,
    default=None,
    help='Datasets only: Add a message to this version. Up to 255 chars.\"text\".'
)
@click.option(
    '-n', '--name',
    type=str,
    default=None,
    help='Datasets only: Add a name to this version. Use \"text\".'
)
@click.option(
    '-q', '--quiet',
    is_flag=True,
    help='Minimize chatter from executed commands.'
)
@click.pass_context
@login_required
def datasets_push(ctx,message, name,quiet):
   general_push(ctx,message, name,quiet)

def datasets_clone(ctx, path, directory, include, exclude,suppress_output=False):
    conn = ctx.obj['connection']
    vc = DatasetViewController(conn)

    values = path.split('/')

    if len(values) == 3:
        try:
            account_uid, datasets_dir, dataset_uid = values
            assert (datasets_dir == 'datasets')
        except:
            click.echo('Invalid dataset path. Please use <account_uid>/datasets/<uid>')
            return
    else:
        click.echo('Invalid dataset path. Please use <account_uid>/datasets/<uid>')
        return

    vc.account_uid = account_uid
    vc.dataset_uid = dataset_uid

    # check dataset path, account_uid, dataset_uid
    if directory is None:
        home = os.path.join(os.getcwd(), dataset_uid)
    elif directory == '.':
        home = os.getcwd()
    else:
        home = os.path.join(os.getcwd(), directory)

    # check if the dataset exists
    url_dataset_check = '/accounts/{}/datasets/{}'.format(account_uid, dataset_uid)
    response_data = vc.get(uid='', field_path='',params=url_dataset_check)
    response_code = response_data['status_code']
    if response_code == 200:
        remote_dataset = response_data['data']
    elif response_code == 401 or response_code == 404:
        print('Dataset does not exist.')
        return
    else:
        print('Error: {}'.format(response_code))
        return None

    if not vc.exists_remote(dataset_uid, remote_dataset):
        click.echo('There is no dataset {}/datasets/{} on the server'.format(account_uid, dataset_uid))
        return

    can_create = True
    if vc.exists_local(home):
        can_create = click.confirm('Dataset already exists, overwrite?')
    if not can_create:
        return
    # Authenticate for S3
    s3auth = S3Authenticator(ctx.obj['connection'])
    creds = s3auth.get_s3_credentials(vc.account_uid, 'datasets', vc.dataset_uid)
    if creds['data'] is None:
        print("Unable to get S3 credentials. Exiting.")
        return False
    aws_access_key_id = creds['data']['AccessKeyID']
    aws_secret_access_key = creds['data']['SecretAccessKey']
    aws_session_token = creds['data']['SessionToken']
    aws_util = AWSUtility(aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          aws_session_token=aws_session_token)
    aws_util.suppress_output = suppress_output
    vc.init_endpoint()

    current_version = vc.get(field_path='/version/current')

    if current_version['data'] is None:
        if current_version['status_code'] == 404:
            click.echo('Dataset is without files.')
            vc.save(home)
            return 0
        else:
            click.echo('Could not get information about dataset.')
            return

    if current_version['data']['provider']['uid'] != 'aws-s3':
        click.echo('Unsupported dataset provider')
        return

    vc.save(home)
    s3_from_dir = current_version['data']['version']['path']
    exit_code = aws_util.download_all(home, s3_from_dir)
    if exit_code != 0:
        click.echo('\nError with downloading files.')
        return

    return 0


def general_push(ctx,comment='',name='',suppress_output=False):
    files = glob.glob("*")
    if len(files) < 1:
        click.echo("Cannot find any files in current dir, exiting.")
        return

    ctx.obj['vc'] = DatasetViewController(ctx.obj['connection'])
    vc = ctx.obj['vc']
    vc.init_credentials_retrieval()
    vc.init_endpoint()

    # Before trying to do any upload, make sure user has permission
    # For example, we don't want them to modify a public dataset
    url_dataset_member_check = '/is_member'
    response_data = vc.head(uid='', field_path='', params=url_dataset_member_check)
    if response_data['status_code'] == 404:
        click.echo('You are not authorized to push to this dataset.')
        return

    next_version = vc.get(field_path='/version/next')

    if next_version['data'] is None:
        click.echo('Could not get information about dataset.')
        return

    if next_version['data']['provider']['uid'] != 'aws-s3':
        click.echo('Unsupported dataset provider')
        return

    # Authenticate for S3
    s3auth = S3Authenticator(ctx.obj['connection'])
    creds = s3auth.get_s3_credentials(vc.account_uid, 'datasets', vc.dataset_uid)
    if creds['data'] is None:
        print("Unable to get S3 credentials. Exiting.")
        return False
    aws_access_key_id = creds['data']['AccessKeyID']
    aws_secret_access_key = creds['data']['SecretAccessKey']
    aws_session_token = creds['data']['SessionToken']

    dataset_dir = os.curdir
    s3_push_to_dir = next_version['data']['version']['path']
    aws_util = AWSUtility(aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          aws_session_token=aws_session_token)
    aws_util.suppress_output = suppress_output
    exit_code = aws_util.upload_dir(dataset_dir, s3_push_to_dir, '.onepanel/*')
    if exit_code != 0:
        click.echo('\nError with pushing up files.')
        return

    # Add the users' 'name' and 'comment' to the dataset
    curr_version = next_version['data']['version']['version']
    post_obj = {
        'comment': comment,
        'name': name
    }
    update_dataset_resp = vc.put(field_path='/update_version',post_object=post_obj)
    if update_dataset_resp['status_code'] != 200:
        click.echo('\nError with calling the API. Contact support if this error continues.')
        return

    click.echo('\nPushed up version ' + str(curr_version))


def datasets_download(ctx, path, directory,suppress_output=False):
    if directory is None or directory == '.':
        home = os.getcwd()
    else:
        home = os.path.join(os.getcwd(), directory)

    code = datasets_clone(ctx, path, home, include='*', exclude='',suppress_output=suppress_output)
    if code != 0:
        print("Unable to download!")
        return False

    print('The files have been downloaded to: {dir}'.format(dir=home))
    return True
