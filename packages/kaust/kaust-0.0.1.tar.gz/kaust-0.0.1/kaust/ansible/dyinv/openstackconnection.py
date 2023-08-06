"""This class connects to an OpenStack cluster to find hosts that have to be pacthed
and which services on those hosts should be tested after reboot"""

import json
import os
from openstack import connection

class OpenStackConnection:
    """This class is used to access backend OpenStack cluster. It exports a
    to_json method that will use query passed during constructing this
    class to find hosts on which Ansible should apply patching."""

    def __init__(self):
        """ Create an OpenStack connection.
        query  -  What to fetch from DB
        """
        auth_url = os.getenv('OPENSSTACK_AUTH_URL', 'https://horizon.kaust.edu.sa:15000/v3/')
        self.connection = connection.Connection(auth_url=auth_url,
                                                project_name=os.getenv('OPENSSTACK_PROJECT_NAME', 'admin'),
                                                username=os.getenv('OPENSTACK_USERNAME'),
                                                password=os.getenv('OPENSTACK_PASSWORD'),
                                                user_domain_id=os.getenv('OPENSTACK_USER_DOMAIN_ID', 'default'),
                                                project_domain_id=os.getenv('OPENSTACK_PROJECT_DOMAIN_ID', 'default'))

    def to_json(self):
        """
        This function returns JSON as expected by Ansible to execute its playbooks on.
        """
        hosts = {
            "all": {
                "hosts": self.metadata_server(),
                "vars": {}
            },
            "_meta": {
                "hostvars": {}
            }
        }
        print(json.dumps(hosts, indent=4, sort_keys=False))


    def metadata_server(self):
        """
        This function returns list of hosts on which patching has to be applied.
        """
        # pylint: disable=no-member
        return [s.name for s in self.connection.compute.servers(all_tenants=True) if OpenStackConnection.server_is_patchable(s)]

    @staticmethod
    def server_is_patchable(server):
        """
        This function returns True is server can be patched.
        """
        return OpenStackConnection.patching_is_enabled(server.metadata) and \
               'ACTIVE' in server.status and \
               OpenStackConnection.has_public_ip(server.addresses)

    @staticmethod
    def patching_is_enabled(metadata):
        """
        This function returns True if metadata allows patching.
        """
        return 'PATCHING' not in metadata or metadata['PATCHING'].lower() == 'yes'

    @staticmethod
    def has_public_ip(addresses):
        """
        This function returns True if addresses contains at least one interface starting with '10.'.
        """
        return 'provider1' in addresses and addresses['provider1'][0]['addr'].startswith('10.')
