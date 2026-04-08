import ansible_runner

import core.util.dir as dir

NETWORK_CREATE = "network.create.yaml"
NETWORK_DELETE = "network.delete.yaml"


def create_network(host, name):

    r = ansible_runner.run(
        private_data_dir=dir.BASE_DIR,
        playbook=NETWORK_CREATE,
        extravars={
            "target_host": host,
            "container_name": name,
        },
        json_mode=True,
    )

    if r.rc == 0:
        return True
    else:
        return False


def delete_network(host, name):

    r = ansible_runner.run(
        private_data_dir=dir.BASE_DIR,
        playbook=NETWORK_DELETE,
        extravars={
            "target_host": host,
            "container_name": name,
        },
        json_mode=True,
    )

    if r.rc == 0:
        return True
    else:
        return False
