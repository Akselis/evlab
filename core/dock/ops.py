import ansible_runner

import core.util.dir as dir

OUTPUT_FILE = "evlab.log"

RUN = "dock_run.ansible.yaml"
STOP = "dock_kill.ansible.yaml"


def start_container(host, image, name):

    r = ansible_runner.run(
        private_data_dir=dir.BASE_DIR,
        playbook=RUN,
        extravars={
            "target_host": host,
            "container_image": image,
            "container_name": name,
        },
        json_mode=True,
    )

    if r.rc == 0:
        return True
    else:
        return False


def stop_container(host, name):

    r = ansible_runner.run(
        private_data_dir=dir.BASE_DIR,
        playbook=STOP,
        extravars={
            "target_host": host,
            "container_name": name,
        },
    )

    if r.rc == 0:
        return True
    else:
        return False
