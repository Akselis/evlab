import ansible_runner

import core.util.dir as dir

DOCKER_CONTAINER_PB = "docker.container.yaml"


class ContainerController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
    ):
        pass

    def Run(self, config=None):
        if config is None:
            raise ValueError("Config must be provided")

        r = ansible_runner.run(
            private_data_dir=dir.BASE_DIR,
            playbook=DOCKER_CONTAINER_PB,
            extravars=config,
        )

        if r.rc == 0:
            if isinstance(r, ansible_runner.runner.Runner):
                container_info = {}
                for event in r.events:
                    if (
                        event["event"] == "runner_on_ok"
                        and event["event_data"]["task"] == "Ensure container state"
                    ):
                        # This contains the return value of the docker_container module
                        res = event["event_data"]["res"]
                        if "container" in res:
                            c = res["container"]
                            container_info = {
                                "id": c.get("Id"),
                                "ip": c.get("NetworkSettings", {}).get("IPAddress"),
                                # If using multiple networks, they are under 'Networks'
                                "networks": c.get("NetworkSettings", {}).get(
                                    "Networks", {}
                                ),
                                "ports": c.get("NetworkSettings", {}).get("Ports", {}),
                                "status": c.get("State", {}).get("Status"),
                            }
                            # If the IP is empty at the top level, look inside the first network
                            if not container_info["ip"] and container_info["networks"]:
                                first_net = list(container_info["networks"].values())[0]
                                container_info["ip"] = first_net.get("IPAddress")

                return True, container_info

            else:
                return False, None

        else:
            return False, None


class ContainerConfigProvider:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
    ):
        pass

    def Default(self):
        return {
            "restart": False,
            "paused": False,
            "restart_policy": "no",
            "force_kill": False,
            "keep_volumes": False,
        }

    def Start(self, host, image, name, config=None):
        if config is None:
            config = self.Default()
        config.update(
            {
                "target_host": host,
                "container_image": image,
                "container_name": name,
                "state": "started",
            }
        )

        return config

    def Stop(self, host, name, config=None):
        if config is None:
            config = self.Default()
        config.update(
            {
                "target_host": host,
                "container_name": name,
                "state": "stopped",
            }
        )

        return config

    def Pause(self, host, name, config=None):
        if config is None:
            config = self.Default()
        config.update(
            {
                "target_host": host,
                "container_name": name,
                "state": "started",
                "paused": True,
            }
        )

        return config

    def Unpause(self, host, name, config=None):
        if config is None:
            config = self.Default()
        config.update(
            {
                "target_host": host,
                "container_name": name,
                "state": "started",
                "paused": False,
            }
        )

        return config

    def Destroy(self, host, name, force=False, config=None):
        if config is None:
            config = self.Default()
        config.update(
            {
                "target_host": host,
                "container_name": name,
                "state": "absent",
                "force_kill": force,
            }
        )

        return config
