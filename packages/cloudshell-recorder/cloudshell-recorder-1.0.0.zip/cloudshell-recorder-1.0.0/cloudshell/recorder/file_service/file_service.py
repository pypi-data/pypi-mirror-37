
import os
from zipfile import ZipFile

CLI_NAME = "cli"
SNMP_NAME = "snmp"
REST_NAME = "rest_api"


def create_output_archive(cli_recording, snmp_recording, rest_recording, path, zip_name):
    zip_filename = zip_name

    if not zip_filename.lower().endswith(".zip"):
        zip_filename += ".zip"
    if not snmp_recording and not cli_recording and not rest_recording:
        return
    
    dst_path = os.path.expandvars(path)
    try:
        os.makedirs(dst_path)
    except:
        pass

    zip_file_path = os.path.join(dst_path, zip_filename)
    with ZipFile(zip_file_path, "w") as zip_file:
        if cli_recording:
            zip_file.writestr("{}.{}".format(zip_name, CLI_NAME), cli_recording)
        if rest_recording:
            zip_file.writestr("{}.{}".format(zip_name, REST_NAME), rest_recording)
        if snmp_recording:
            zip_file.writestr("{}.{}".format(zip_name, SNMP_NAME), snmp_recording)
    return zip_file_path
