"""This class connects to a SCUBA database to read hosts that have to be pacthed
and which services on those hosts should be tested after reboot"""

from collections import defaultdict
import os
import json
import pymssql


SCUBA_QUERY = """
    SELECT * FROM V_SERVER where
    {}
    Administeredby = 'itlinuxteam' and
    lifecycle_status = 'commissioned' and
    virtualization_name != 'openstack';"""


DMZ_CLAUSE = "Primary_IPAddress like '10.254.21.%' and"

# pylint: disable=too-few-public-methods
class ScubaConnection:
    """This class is used to access backend SCUBA database. It exports a
    to_json method that will use query passed during constructing this
    class to find hosts on which Ansible should apply patching."""

    def __init__(self):
        """ Create a SCUBA coonection.
        query  -  What to fetch from DB
        """
        self.query = ScubaConnection.get_query_for(os.getenv('APF_SCUBDA_NODES', 'all'))

    def to_json(self):
        """
        This function returns JSON as expected by Ansible to execute its playbooks on.
        """
        # pylint: disable=c-extension-no-member
        with pymssql.connect(server=os.getenv('SCUBA_HOST'),
                             user=os.getenv('SCUBA_USERNAME'),
                             password=os.getenv('SCUBA_PASSWORD'),
                             database=os.getenv('SCUBA_DATABASE'),
                             tds_version=os.getenv('SCUBA_TDS_VERSION')) as connection:
            with connection.cursor(as_dict=True) as cursor:
                agroup = defaultdict(list)
                meta_json = {}
                temp_chart_table = {}

                cursor.execute(self.query)
                for row in cursor.fetchall():
                    automation_service = row['automation_service']
                    agroup['all'].append(row['Host_Name'])
                    if row['automation_group'] and row['automation_group'].strip():
                        agroup[row['automation_group']].append(row['Host_Name'])
                    temp_chart_table.update({row['Host_Name'] : {"service_tag" : automation_service.split(',')}})

                group_json = {"hosts" : agroup['all'], "vars": {}}
                host_json = {"hostvars" : temp_chart_table}
                meta_json = {"all" : group_json,
                             'centos_nodes': agroup['CentOS'],
                             'rhel_nodes': agroup['RedHat'],
                             'ubuntu_nodes': agroup['Ubuntu'],
                             "_meta" : host_json}

                return json.dumps(meta_json, indent=4, sort_keys=False)

    @staticmethod
    def get_query_for(nodes):
        """
        This function returns SQL query to perform based on nodes.
        """
        clause = ''
        if nodes == 'dmz':
            clause = DMZ_CLAUSE
        return SCUBA_QUERY.format(clause)
