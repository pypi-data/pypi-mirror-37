from arkindex import DEFAULT_HOST
from arkindex.conf import LocalConf
from arkindex.client import ArkindexAPI
import getpass
import uuid
import click

conf = LocalConf()


@click.group()
@click.option(
    '--profile',
    default='default',
    help='A reference name for your profile on this Arkindex host.',
)
@click.option(
    '--verify-ssl/--no-verify-ssl',
    default=True,
)
@click.pass_context
def main(context, profile, verify_ssl):
    context.ensure_object(dict)

    # Load existing profile from local configuration
    context.obj['profile_name'] = profile
    context.obj['profile'] = conf.profiles.get(profile)

    context.obj['verify_ssl'] = verify_ssl
    if not verify_ssl:
        # Warn once and disable urllib3's dozens of warnings
        click.echo('Will perform insecure HTTPS requests without checking SSL certificates.')
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@main.command()
@click.option(
    '--host',
    default=DEFAULT_HOST,
    prompt='Arkindex hostname',
    help='An Arkindex hostname to login.',
)
@click.option(
    '--email',
    prompt='Your email',
    help='Your account\'s email on this Arkindex host',
)
@click.pass_context
def login(context, host, email):
    '''
    Login on an arkindex host to get the credentials
    '''

    # Read password
    password = getpass.getpass(prompt='Your password: ')

    # Try to login on the Arkindex server
    api = ArkindexAPI(host=host, verify_ssl=context.obj['verify_ssl'])
    try:
        resp = api.login(email, password)
    except Exception as e:
        click.echo('Login failed: {}'.format(e))
        return

    # Save token in local profile
    try:
        token = resp['auth_token']
    except KeyError:
        click.echo('Login successful, but the API did not return token info. Please contact a developer.')
        return
    if token is None:
        click.echo('Login successful, but no token is available. Please ask an admin.')
        return
    conf.save_profile(context.obj['profile_name'], host=host, email=email, token=token)
    conf.write()

    click.echo('Login successful !')


@main.command()
@click.argument(
    'corpus',
)
@click.argument(
    'files',
    nargs=-1,
    type=click.Path(exists=True),
)
@click.option(
    '--start/--no-start',
    help='Start a data import after a file is uploaded',
    default=True,
)
@click.option(
    '--mode',
    default='pdf',
    type=click.Choice(['pdf', 'images']),
    help='Data import type to start',
)
@click.pass_context
def upload(context, files, corpus, start, mode):
    '''
    Upload one or multiple files on the Arkindex host
    '''

    # Load the user profile
    profile = context.obj['profile']
    if profile is None:
        click.echo('Missing arkindex profile, please login first')
        return

    # Check auth
    # TODO: this should be automated once we have several commands
    try:
        api = ArkindexAPI(host=profile['host'], token=profile['token'], verify_ssl=context.obj['verify_ssl'])
        user = api.whoami()
        click.echo('Authentified as {} on {}'.format(user['email'], profile['host']))
    except Exception as e:
        click.echo('Authentification failed for profile {}: {}'.format(context.obj['profile_name'], e))
        return

    try:
        corpora = api.get_corpora()
    except Exception as e:
        click.echo('An error occured while fetching corpora: {}'.format(str(e)))
        return

    try:
        try:
            corpus_id = str(uuid.UUID(corpus))
            found_corpora = [c for c in corpora if c['id'] == corpus_id]
        except ValueError:
            found_corpora = [c for c in corpora if corpus.lower().strip() in c['name'].lower()]

        if len(found_corpora) == 0:
            click.echo('Corpus "{}" not found'.format(corpus))
            return
        elif len(found_corpora) > 1:
            click.echo('Multiple matching corpora for "{}". Please retry with a full name or ID'.format(corpus))
            click.echo('Matched corpora: "{}"'.format('", "'.join(c['name'] for c in found_corpora)))
            return

        corpus_id = found_corpora[0]['id']
    except Exception as e:
        click.echo('An error occured while matching corpora: {}'.format(str(e)))

    import_ids = []

    with click.progressbar(files, label='Uploading files') as bar:
        for local_file in bar:
            # Upload file
            try:
                datafile = api.upload_file(corpus_id, local_file)
            except Exception as e:
                click.echo('An error occured while uploading file {}: {}'.format(local_file, str(e)))
                continue

            if not start:
                continue

            # Start import
            try:
                dataimport = api.import_from_files(mode, [datafile['id']])
                import_ids.append(dataimport['id'])
            except Exception as e:
                click.echo('An error occured while starting the import process for file {}: {}'.format(
                    local_file, str(e)))
                continue

    if start:
        click.echo('Started {} imports with IDs {}'.format(len(import_ids), ', '.join(import_ids)))
    else:
        click.echo('All uploaded !')
