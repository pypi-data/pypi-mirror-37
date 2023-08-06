"""This class returns SMT virtual servers for testing"""

import json

INVENTORY = {
    "_meta": {
        "hostvars": {
            "10.254.145.120": {
                "service_tag" : ['httpd']
            },
            "10.254.145.121": {
                "service_tag" : ['httpd', 'sshd']
            },
            "10.254.145.122": {
                "service_tag" : ['httpd', 'sshd']
            }
        }
    },
    "rhel_nodes": ['10.254.145.120', '10.254.145.121', '10.254.145.122', '10.254.146.120']
}

class TestInventory:
    """This class is used to access SMT test nodes."""

    # pylint: disable=no-self-use
    def to_json(self):
        """
        This function returns JSON as expected by Ansible to execute its playbooks on.
        """
        return json.dumps(INVENTORY, indent=4)
