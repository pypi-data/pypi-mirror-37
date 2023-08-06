"""This class returns SMT physical workstations for testing"""

import json

INVENTORY = {
    "_meta": {
        "hostvars": {
            "kw13804": {
                "service_tag" : ['autofs', 'filebeat', 'metricbeat']
            },
            "kw14420": {
                "service_tag" : ['autofs', 'filebeat', 'metricbeat']
            },
            "kw14820": {
                "service_tag" : ['autofs', 'filebeat', 'metricbeat']
            },
            "kw14980": {
                "service_tag" : ['autofs', 'filebeat', 'metricbeat']
            },
            "kw60017": {
                "service_tag" : ['autofs', 'filebeat', 'metricbeat']
            },
        }
    },
    "ubuntu_nodes": ['kw13804', 'kw14420', 'kw14820', 'kw14980', 'kw60017']
}

class SmtPsw:
    """This class is used to access SMT test nodes."""

    # pylint: disable=no-self-use
    def to_json(self):
        """
        This function returns JSON as expected by Ansible to execute its playbooks on.
        """
        return json.dumps(INVENTORY, indent=4)
