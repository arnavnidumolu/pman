"""
Helper class for get_data and put_data
Establishes swift connection and returns a connection object
"""

import os
import configparser
from keystoneauth1.identity import v3
from keystoneauth1 import session
from swiftclient import service as swift_service

def _createSwiftService(configPath):
    config = configparser.ConfigParser()
    try:
        f = open(configPath, 'r')
        config.readfp(f)
    finally:
        f.close()

    options = {
        'auth_version':         3,
        'os_auth_url':          config['AUTHORIZATION']['osAuthUrl'],
        'identity_provider':    config['PROJECT']['identityProvider'],
        'protocol':             config['PROJECT']['protocol'],
        'os_username':          config['AUTHORIZATION']['username'],
        'os_password':          config['AUTHORIZATION']['password'],
        'os_project_domain_name':    config['PROJECT']['osProjectDomain'],
        'os_project_name':      config['PROJECT']['osProjectName'],
        'client_id':            config['SECRET']['clientId'],
        'client_secret':        config['SECRET']['clientSecret'],
        'access_token_endpoint':     config['ENDPOINT']['accessTokenEndpoint'],
        'discovery_endpoint':        config['ENDPOINT']['discoveryEndpoint']
    }

    auth_swift = v3.oidc.OidcPassword(
        options['os_auth_url'],
        identity_provider=options['identity_provider'],
        protocol=options['protocol'],
        client_id=options['client_id'],
        client_secret=options['client_secret'],
        access_token_endpoint=options['access_token_endpoint'],
        discovery_endpoint=options['discovery_endpoint'],
        username=options['os_username'],
        password=options['os_password'],
        project_name=options['os_project_name'],
        project_domain_name=options['os_project_domain_name']
    )

    session_client = session.Session(auth=auth_swift)
    service = swift_service.Connection(session=session_client)
    return service
    
def _deleteEmptyDirectory(key):
    """
    Deletes the empty directory created by Swift in the parent directory
    """

    directoryPath = os.path.join(os.path.dirname(__file__), '../%s'%key)
    try:
        os.rmdir(directoryPath)
        print("Temporary directory %s deleted"%key)
    except:
        print("No temporary directory found")
