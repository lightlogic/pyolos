import click
import configparser
from dotenv import load_dotenv
import json
import os
import requests
from datetime import datetime
import time


from classes.endpoint import Endpoint
from classes.bearerauth import BearerAuth
from classes.dlcm_deposit import DlcmDeposit


class Config(object):

    def __init__(self):
        self.verbose = False
        self.api_setup = configparser.ConfigParser()
        cwd = os.path.dirname(__file__)
        conf_path= os.path.join(cwd, "conf")
        self.api_setup.read(os.path.join(conf_path, 'dlcm_resources.ini'))
        self.org_ident = configparser.ConfigParser()
        self.org_ident.read(os.path.join(conf_path,'organisational_unit.ini'))
        load_dotenv()
        self.myToken = os.getenv('token')
        self.strt_time = time.time()


# passing config object to sub-commands
pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--verbose', is_flag=True,
              help='Showing various details of the process.')
@pass_config
def cli(config, verbose):
    """Command line interface to use OLOS preservation infrastructure."""
    config.verbose = verbose

@cli.command()
@click.option('--access-level', help="The access level of the deposit. Values: PUBLIC, RESTRICTED, CLOSED")
@click.option('--datasensitivity', help="The data sensitivity of the deposit. Values: UNDEFINED, BLUE, GREEN, YELLOW, ORANGE, RED, CRIMSON")
@click.option('--description', help="The description of the deposit.")
@click.option('--pubdate', help="The publication date of the deposit. Format: yyyy-MM-dd")
@click.option('--title', help="The title of the deposit.")
@click.argument('output', type=click.File('w'), default='-',
                required=False)
@pass_config
def deposit_create(config, access_level, datasensitivity, description, pubdate, title, output):
    """POST new deposit, a resource used as a container to group several datasets (files) to be submited. 
       [OUTPUT] allows the output to be saved to a file.
       If no argument is provided, the output is send to stout."""

    verbose_message = "\n[Verbose mode]\n"
    if (title is not None) and (description is not None):
        preingest_deposit_create_endpoint = Endpoint(
            config.api_setup['Server']['protocol'],
            config.api_setup['Server']['root_context'],
            config.api_setup['Modules']['preingest'],
            'deposits')
        if access_level is None:
            verbose_message += 'No access level specified : using default (' + \
                config.api_setup['Deposit_DEFAULT']['access_level'] + ')\n'
            access_level = config.api_setup['Deposit_DEFAULT']['access_level']
        if datasensitivity is None:
            verbose_message += 'No data sensitivity specified: using default (' + \
                config.api_setup['Deposit_DEFAULT']['data_sensitivity'] + ')\n'
            datasensitivity = config.api_setup['Deposit_DEFAULT']['data_sensitivity']
        if pubdate is None:
            verbose_message += 'No publication date specified : using NOW.'
            pubdate = datetime.today().strftime('%Y-%m-%d')
        new_deposit = DlcmDeposit(access_level,
                                  datasensitivity,
                                  title,
                                  description,
                                  config.org_ident['Org']['org_unit_id'],
                                  pubdate)
        deposit_json_str = json.dumps(new_deposit.__dict__)
        response = requests.post(
            preingest_deposit_create_endpoint.getRessourceURL(),
            auth=BearerAuth(config.myToken),
            json=new_deposit.__dict__
        )
        if response.status_code == 201:
            click.echo(response.content, file=output)
        else:
            click.echo(response.content)

        if config.verbose:
            click.echo(verbose_message)
            click.echo('--- took %s seconds ---' %
                       (time.time() - config.strt_time))
    else:
        click.echo(
            '\nERROR: A title and a description are mandatory. \n\nAborted !', err=True)

@cli.command()
@click.option('--resid', help="Deposit resource ID.")
# output filename
# "default='-'" means that without the argument, it prints out to standardOutput
@click.argument('output', type=click.File('w'), default='-',
                required=False)
@pass_config
def deposit_delete(config, resid, output):
    """DELETE deposit by passing its resource Id. 
       [OUTPUT] allows the output to be saved to a file.
       If no argument is provided, the output is send to stout."""

    if resid is not None:
        verbose_message = "\n[Verbose mode]\n"
        preingest_deposit_delete_endpoint = Endpoint(
            config.api_setup['Server']['protocol'],
            config.api_setup['Server']['root_context'],
            config.api_setup['Modules']['preingest'],
            'deposits',
            resid)
        response = requests.delete(
            preingest_deposit_delete_endpoint.getRessourceURL(),
            auth=BearerAuth(config.myToken))
        if response.status_code == 200:
            click.echo('\nDeposit ' + resid + ' was successfully deleted.')
        elif response.status_code == 404:
            click.echo('\nNot found: deposit ' + resid +
                       ' does not seem to exist.', err=True)
        else:
            click.echo(response.status_code)

        if config.verbose:
            click.echo(verbose_message)
            click.echo('--- took %s seconds ---' %
                       (time.time() - config.strt_time))
    else:
        click.echo("\nError: Missing option 'resid'. \n\nAborted !", err=True)

@cli.command()
@click.option('--resid', help="Deposit resource ID.")
# output filename
# "default='-'" means that without the argument, it prints out to standardOutput
@click.argument('output', type=click.File('w'), default='-',
                required=False)
@pass_config
def deposit_meta(config, resid, output):
    """GET deposit's metadata by passing its resource Id. 
       [OUTPUT] allows the output to be saved to a file.
       If no argument is provided, the output is send to stout."""
    if resid is not None:    
        if config.verbose:
            verbose_message = "\n[Verbose mode]\n"

        preingest_deposit_meta_endpoint = Endpoint(
            config.api_setup['Server']['protocol'],
            config.api_setup['Server']['root_context'],
            config.api_setup['Modules']['preingest'],
            'deposits',
            resid)
        response = requests.get(
            preingest_deposit_meta_endpoint.getRessourceURL(),
            auth=BearerAuth(config.myToken))
        if response.status_code == 200:
            click.echo(response.content, file=output)
        else:
            click.echo(response.content)

        if config.verbose:
            click.echo(verbose_message)
            click.echo('--- took %s seconds ---' %
                        (time.time() - config.strt_time))
    else:
        click.echo("\nError: Missing option 'resid'. \n\nAborted !", err=True)


@cli.command()
@click.option('--file-category', default='Primary', help="The category size of the data file. Values: Primary, Secondary, Package, Software. Default: Primary")
@click.option('--file-type', default='Digitalized', help="The sub-category size of the data file. Available values depend on the category. See Data File Details: https://sandbox.dlcm.ch/administration/docs/DLCM-APIs.html#data-file. Default: Digitalized")
@click.argument('deposit-id')
@click.argument('file-path', type=click.Path(exists='True', file_okay='True'))
@click.argument('output', type=click.File('w'), default='-',
                required=False)
@pass_config
def deposit_upload(config, file_category, file_type, deposit_id, file_path, output):
    """Add a new file to an existing deposit.
       [DEPOSIT-ID] Resource Id from the deposit. 
       [FILE-PATH] Full path to the file to add.
       [OUTPUT] allows the output to be saved to a file.
       If no argument is provided, the output is send to stout."""

    verbose_message = "\n[Verbose mode]\n"
    preingest_deposit_upload_endpoint = Endpoint(
        config.api_setup['Server']['protocol'],
        config.api_setup['Server']['root_context'],
        config.api_setup['Modules']['preingest'],
        'deposits',
        deposit_id)
    dataParams = {'category': file_category, 'type': file_type}

    with click.open_file(file_path, mode='rb') as payload:
        response = requests.post(
            preingest_deposit_upload_endpoint.getRessourceURL()+'/upload',
            auth=BearerAuth(config.myToken),
            params=dataParams,
            files=dict(file=payload)
        )
    verbose_message += "POST: " + response.url
    click.echo(response.status_code)
    if response.status_code == 200:
        click.echo(response.content, file=output)
    else:
        click.echo(response.content)

    if config.verbose:
        click.echo(verbose_message)
        click.echo('--- took %s seconds ---' %
                    (time.time() - config.strt_time))

@cli.command()
@click.option('--resid', help="Deposit resource ID.")
# output filename
# "default='-'" means that without the argument, it prints out to standardOutput
@click.argument('output', type=click.File('w'), default='-',
                required=False)
@pass_config
def deposit_approve(config, resid, output):
    """Submit deposit for approval by passing its resource Id. 
       [OUTPUT] allows the output to be saved to a file.
       If no argument is provided, the output is send to stout."""

    if resid is not None:
        verbose_message = "\n[Verbose mode]\n"
        preingest_deposit_approve_endpoint = Endpoint(
            config.api_setup['Server']['protocol'],
            config.api_setup['Server']['root_context'],
            config.api_setup['Modules']['preingest'],
            'deposits',
            resid)
        response = requests.post(
            preingest_deposit_approve_endpoint.getRessourceURL()+'/approve',
            auth=BearerAuth(config.myToken))
        verbose_message += "POST: " + response.url

        if response.status_code == 200:
            click.echo('\nDeposit ' + resid + ' was successfully approved.')
        elif response.status_code == 304:
            click.echo('\nDeposit ' + resid + ' was allready approved. Nothing changed.')
        elif response.status_code == 404:
            click.echo('\nNot found: deposit ' + resid +
                       ' does not seem to exist.', err=True)
        else:
            click.echo(response.status_code)

        if config.verbose:
            click.echo(verbose_message)
            click.echo('--- took %s seconds ---' %
                       (time.time() - config.strt_time))
    else:
        click.echo("\nError: Missing option 'resid'. \n\nAborted !", err=True)
