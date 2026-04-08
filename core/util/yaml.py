from ruamel.yaml import YAML


class EvLabYAML:
    file: str = ""

    def __init__(self, file):
        self.file = file
        self.yaml = YAML()
        self.yaml.preserve_quotes = True
        with open(self.file, "r") as f:
            self.data = self.yaml.load(f)

    def dump(self, data=None, stream=None):
        if data is None and self.data is not None:
            data = self.data
        elif self.data is None:
            raise ValueError("No data to dump")

        with open(self.file, "w") as f:
            self.yaml.dump(data, f)
