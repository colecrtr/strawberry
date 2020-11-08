import typing


class Fork:
    def __init__(self, **paths_to_bools: bool):
        self.paths: list[str] = [
            key for key, value in paths_to_bools.items() if value is True
        ]

        if not self.paths:
            raise ValueError("No paths evaluated to True")

    def __call__(self, **paths_to_values: typing.Any):
        for path in self.paths:
            try:
                return paths_to_values[path]
            except KeyError:
                pass

        raise ValueError("No available path to a value")
