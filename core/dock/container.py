import ansible_runner

import core.util.dir as dir

CONTAINER_START = "container.start.yaml"
CONTAINER_STOP = "container.stop.yaml"


def start_container(host, image, name):

    r = ansible_runner.run(
        private_data_dir=dir.BASE_DIR,
        playbook=CONTAINER_START,
        extravars={
            "target_host": host,
            "container_image": image,
            "container_name": name,
        },
    )

    if r.rc == 0:
        return True
    else:
        return False


def stop_container(host, name):

    r = ansible_runner.run(
        private_data_dir=dir.BASE_DIR,
        playbook=CONTAINER_STOP,
        extravars={
            "target_host": host,
            "container_name": name,
        },
    )

    if r.rc == 0:
        return True
    else:
        return False
