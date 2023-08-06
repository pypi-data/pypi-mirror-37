import click
import pkg_resources

from cloudshell.recorder.recorder_orchestrator import RecorderOrchestrator


@click.group()
def cli():
    pass


@cli.command()
def version():
    """
    Displays the cloudshell-recorder version
    """

    click.echo(
        u'cloudshell-recorder version ' + pkg_resources.get_distribution('cloudshell-recorder').version)


@cli.command()
@click.argument(u'ip')
@click.option(u'--cli-user', help="CLI user")
@click.option(u'--cli-password', help="CLI password")
@click.option(u'--cli-enable-password', help="CLI enable password")
@click.option(u'--cli-session-type', default="auto",
              help="CLI session type: auto (for autodetect session type), ssh, telnet")
@click.option(u'--rest-user', help="REST user")
@click.option(u'--rest-password', help="REST password")
@click.option(u'--rest-token', help="REST token")
@click.option(u'--snmp-community', help="SNMP v1 or v2 community")
@click.option(u'--snmp-user', help="SNMP v3 user")
@click.option(u'--snmp-password', help="SNMP password or auth")
@click.option(u'--snmp-private-key', help="SNMP privacy key")
@click.option(u'--snmp-auth-protocol', default="NONE",
              help="SNMP auth encryption type: SHA, MD5, SHA224, SHA256, SHA384, SHA512, NONE. Default is NONE.")
@click.option(u'--snmp-priv-protocol', default="NONE",
              help="SNMP privacy encryption type: DES, 3DES, AES, AES128, AES192, AES192BLMT, AES256, AES256BLMT, "
                   "NONE. Default is NONE.")
@click.option(u"--record-type", default="all", help="Defines what will be recorded. "
                                                    "Possible values: cli, rest, snmp, all. Default is all")
@click.option(u'--snmp-auto-detect-vendor', is_flag=True, help="Enables auto detect of device manufacturer")
@click.option(u'--snmp-record-oids', default="shells_based",
              help="Specify an OID template file for adding records 'template:PATH_TO_FILE' "
                   "or set it to 'all' to record entire device. "
                   "Default is 'shells_based', which will record all OIDs used by the shells.")
@click.option(u'--destination-path', default="%APPDATA%\\Quali\\Recordings",
              help="Destination path, i.e. %APPDATA%\\Quali\\Recordings")
@click.option(u'--snmp-timeout', default=2000, help="SNMP timeout")
@click.option(u'--snmp-retries', default=2, help="Number of SNMP retries")
@click.option(u'--snmp-bulk', is_flag=False, help="Add to use snmpbulk for better performance")
@click.option(u'--snmp-bulk-repetitions', default=25, help="Number of snmpbulk repetitions")
def new(ip,
        destination_path,
        record_type="all",
        cli_user=None,
        cli_password=None,
        cli_enable_password=None,
        cli_session_type="auto",
        rest_user=None,
        rest_password=None,
        rest_token=None,
        snmp_community=None,
        snmp_user=None,
        snmp_password=None,
        snmp_private_key=None,
        snmp_auth_protocol=None,
        snmp_priv_protocol=None,
        snmp_record_oids=None,
        snmp_timeout=2000,
        snmp_retries=2,
        snmp_bulk=False,
        snmp_bulk_repetitions=25,
        snmp_auto_detect_vendor=False):
    """
    Creates a new device recording based on a template
    """

    try:
        RecorderOrchestrator(ip, recording_type=record_type, destination_path=destination_path).new_recording(
            cli_user=cli_user, cli_password=cli_password,
            cli_enable_password=cli_enable_password,
            cli_session_type=cli_session_type,
            rest_user=rest_user,
            rest_password=rest_password,
            rest_token=rest_token,
            snmp_community=snmp_community,
            snmp_user=snmp_user, snmp_password=snmp_password,
            snmp_private_key=snmp_private_key,
            snmp_auth_protocol=snmp_auth_protocol,
            snmp_priv_protocol=snmp_priv_protocol,
            snmp_record=snmp_record_oids,
            snmp_timeout=snmp_timeout,
            snmp_bulk=snmp_bulk,
            snmp_retries=snmp_retries,
            snmp_bulk_repetitions=snmp_bulk_repetitions,
            snmp_auto_detect_vendor=snmp_auto_detect_vendor)
    except Exception as e:
        click.secho(e.message)
        with click.Context(new) as context:
            click.echo(new.get_help(context))
            return
